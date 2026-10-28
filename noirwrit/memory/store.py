"""Chunk, embed, index, retrieve, and check novelty.

The "unlimited context" trick: anything the user gives (files, pasted text) and
everything Noirwrit writes is split into 500-token chunks with 50 tokens of
overlap, embedded, and stored. A scene prompt pulls only the top-k chunks for
its beat, so the 2048-token window never has to hold the whole story.

The index is exact cosine search over a float32 matrix. A story library holds
thousands to low hundreds of thousands of chunks, where brute force is a few
milliseconds and needs no extra native dependency.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from noirwrit.memory.db import DB
from noirwrit.memory.embed import Embedder, get_embedder

CHUNK_TOKENS = 500
CHUNK_OVERLAP = 50
NOVELTY_COSINE = 0.85
NOVELTY_NGRAM = 0.25
NGRAM_N = 5


class Tokenish:
    """Tokenizer adapter. Uses the Noirwrit BPE when present, else words."""

    def __init__(self):
        self.tok = None
        try:
            from noirwrit.tokenizer.train_tokenizer import TOKENIZER_PATH, load_tokenizer

            if TOKENIZER_PATH.exists():
                self.tok = load_tokenizer()
        except Exception:
            self.tok = None

    def split(self, text: str) -> list[tuple[int, int]]:
        """Character spans of each token."""
        if self.tok is not None:
            return list(self.tok.encode(text).offsets)
        return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


_tokenish: Tokenish | None = None


def chunk_text(text: str, size: int = CHUNK_TOKENS, overlap: int = CHUNK_OVERLAP) -> list[str]:
    global _tokenish
    if _tokenish is None:
        _tokenish = Tokenish()
    spans = _tokenish.split(text)
    if not spans:
        return []
    out = []
    step = max(size - overlap, 1)
    for i in range(0, len(spans), step):
        part = spans[i:i + size]
        out.append(text[part[0][0]:part[-1][1]].strip())
        if i + size >= len(spans):
            break
    return [c for c in out if c]


def ngram_hashes(text: str, n: int = NGRAM_N) -> set[int]:
    words = re.findall(r"[a-z']+", text.lower())
    out = set()
    for i in range(len(words) - n + 1):
        d = hashlib.blake2b(" ".join(words[i:i + n]).encode(), digest_size=8).digest()
        out.add(int.from_bytes(d, "little", signed=True))
    return out


@dataclass
class Hit:
    chunk_id: int
    score: float
    text: str
    source: str
    story_id: int | None
    kind: str


@dataclass
class NoveltyReport:
    novel: bool
    max_cosine: float
    ngram_overlap: float
    closest_story: int | None
    reason: str = ""


class Memory:
    def __init__(self, db: DB, embedder: Embedder | None = None):
        self.db = db
        self.emb = embedder or get_embedder()
        self._ids: np.ndarray | None = None
        self._mat: np.ndarray | None = None
        self._meta: list[tuple[int | None, str]] = []

    # Index ----------------------------------------------------------------

    def _invalidate(self) -> None:
        self._mat = None

    def _load(self) -> None:
        if self._mat is not None:
            return
        rows = self.db.query("SELECT id, story_id, kind, embedding FROM chunks ORDER BY id")
        if not rows:
            self._ids = np.zeros(0, dtype=np.int64)
            self._mat = np.zeros((0, self.emb.dim), dtype=np.float32)
            self._meta = []
            return
        self._ids = np.array([r["id"] for r in rows], dtype=np.int64)
        self._mat = np.stack([np.frombuffer(r["embedding"], dtype=np.float32) for r in rows])
        self._meta = [(r["story_id"], r["kind"]) for r in rows]

    # Ingest ---------------------------------------------------------------

    def ingest_text(self, text: str, source: str, story_id: int | None = None, kind: str = "context") -> int:
        """Chunk, embed and store any amount of text. Returns the chunk count."""
        chunks = chunk_text(text)
        if not chunks:
            return 0
        n = 0
        for i in range(0, len(chunks), 64):
            batch = chunks[i:i + 64]
            vecs = self.emb.embed(batch)
            self.db.conn.executemany(
                "INSERT INTO chunks(source, story_id, kind, text, embedding) VALUES (?, ?, ?, ?, ?)",
                [(source, story_id, kind, c, v.astype(np.float32).tobytes()) for c, v in zip(batch, vecs, strict=True)],
            )
            n += len(batch)
        if story_id is not None and kind in ("chapter", "scene"):
            hashes = ngram_hashes(text)
            self.db.conn.executemany("INSERT INTO ngrams(story_id, hash) VALUES (?, ?)", [(story_id, h) for h in hashes])
        self.db.conn.commit()
        self._invalidate()
        return n

    def ingest_file(self, path: str | Path, story_id: int | None = None) -> int:
        p = Path(path)
        suffix = p.suffix.lower()
        if suffix in (".txt", ".md", ".markdown", ".text", ""):
            text = p.read_text(errors="replace")
        elif suffix == ".json":
            text = json.dumps(json.loads(p.read_text()), indent=1)
        elif suffix == ".epub":
            text = _epub_text(p)
        else:
            raise ValueError(f"unsupported file type: {suffix}")
        return self.ingest_text(text, source=p.name, story_id=story_id, kind="context")

    # Retrieval ------------------------------------------------------------

    def search(self, query: str, k: int = 5, story_id: int | None = None, include_global: bool = True,
               kinds: tuple[str, ...] | None = None, exclude_story: int | None = None) -> list[Hit]:
        self._load()
        assert self._mat is not None and self._ids is not None
        if len(self._ids) == 0:
            return []
        q = self.emb.embed_one(query)
        scores = self._mat @ q
        mask = np.ones(len(scores), dtype=bool)
        for i, (sid, kind) in enumerate(self._meta):
            if story_id is not None:
                ok = sid == story_id or (include_global and sid is None)
            else:
                ok = True
            if exclude_story is not None and sid == exclude_story:
                ok = False
            if kinds and kind not in kinds:
                ok = False
            mask[i] = ok
        scores = np.where(mask, scores, -np.inf)
        top = np.argsort(-scores)[:k]
        hits = []
        for i in top:
            if not np.isfinite(scores[i]):
                continue
            r = self.db.one("SELECT id, text, source, story_id, kind FROM chunks WHERE id=?", (int(self._ids[i]),))
            if r:
                hits.append(Hit(r["id"], float(scores[i]), r["text"], r["source"], r["story_id"], r["kind"]))
        return hits

    # Novelty --------------------------------------------------------------

    def novelty(self, text: str, story_id: int | None = None, cos_threshold: float = NOVELTY_COSINE,
                ngram_threshold: float = NOVELTY_NGRAM) -> NoveltyReport:
        """Compare text against every other story Noirwrit has written."""
        self._load()
        assert self._mat is not None
        max_cos, closest = 0.0, None
        idx = [i for i, (sid, kind) in enumerate(self._meta)
               if sid is not None and sid != story_id and kind in ("chapter", "scene")]
        if idx:
            sub = self._mat[idx]
            # Compare chunk by chunk so a long text matches its closest passage.
            vecs = self.emb.embed(chunk_text(text) or [text])
            sims = vecs @ sub.T
            j = np.unravel_index(int(np.argmax(sims)), sims.shape)
            max_cos = float(sims[j])
            closest = self._meta[idx[j[1]]][0]

        hashes = ngram_hashes(text)
        overlap = 0.0
        if hashes:
            best = 0
            hl = list(hashes)
            counts: dict[int, int] = {}
            for i in range(0, len(hl), 500):
                part = hl[i:i + 500]
                q = f"SELECT story_id, COUNT(DISTINCT hash) AS c FROM ngrams WHERE hash IN ({','.join('?' * len(part))})"
                args: list = list(part)
                if story_id is not None:
                    q += " AND story_id != ?"
                    args.append(story_id)
                q += " GROUP BY story_id"
                for r in self.db.query(q, args):
                    counts[r["story_id"]] = counts.get(r["story_id"], 0) + r["c"]
            if counts:
                sid, best = max(counts.items(), key=lambda kv: kv[1])
                overlap = best / len(hashes)
                if closest is None:
                    closest = sid

        reasons = []
        if max_cos > cos_threshold:
            reasons.append(f"cosine {max_cos:.2f} > {cos_threshold}")
        if overlap > ngram_threshold:
            reasons.append(f"{NGRAM_N}-gram overlap {overlap:.0%} > {ngram_threshold:.0%}")
        return NoveltyReport(not reasons, max_cos, overlap, closest, "; ".join(reasons))


# Spec matching ------------------------------------------------------------

CATEGORICAL = ("genre", "era", "setting", "detective_type", "pov", "tone", "vibe")
FREE_TEXT = ("victim", "culprit", "motive", "twist", "premise")


def _norm(v) -> str:
    return re.sub(r"\s+", " ", str(v or "").strip().lower())


def match_spec(new: dict, stored: list[tuple[int, dict]], emb: Embedder | None = None,
               threshold: float = 0.6) -> dict | None:
    """Find the most similar stored spec. Returns {spec_id, score, matched} or None.

    The UI uses this to ask "continue, vary, or start fresh?" and shows which
    fields matched.
    """
    emb = emb or get_embedder()
    best = None
    for sid, old in stored:
        matched, total, score = [], 0, 0.0
        for f in CATEGORICAL:
            if _norm(new.get(f)) or _norm(old.get(f)):
                total += 1
                if _norm(new.get(f)) and _norm(new.get(f)) == _norm(old.get(f)):
                    score += 1
                    matched.append(f)
        for f in FREE_TEXT:
            a, b = _norm(new.get(f)), _norm(old.get(f))
            if a or b:
                total += 1
                if a and b:
                    sim = float(emb.embed_one(a) @ emb.embed_one(b))
                    if a == b or sim > 0.8:
                        score += 1
                        matched.append(f)
                    elif sim > 0.6:
                        score += 0.5
        if not total:
            continue
        s = score / total
        if best is None or s > best["score"]:
            best = {"spec_id": sid, "score": round(s, 3), "matched": matched}
    if best and best["score"] >= threshold:
        return best
    return None


def _epub_text(path: Path) -> str:
    from ebooklib import ITEM_DOCUMENT, epub

    book = epub.read_epub(str(path))
    parts = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        html = item.get_content().decode("utf-8", errors="replace")
        parts.append(re.sub(r"<[^>]+>", " ", html))
    return re.sub(r"\s+\n", "\n", "\n\n".join(parts))
