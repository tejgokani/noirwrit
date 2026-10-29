"""Story engine: plan a story, then write chapters scene by scene.

Prompt for each scene = a compact story header + previous chapter summary +
retrieved memory chunks + bible slice + the tail of the previous scene + the
beat's prose lead-in. The model continues the lead-in. Every scene is saved as
soon as it is written, so a crash loses at most the scene in progress.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from dataclasses import dataclass

from noirwrit.memory.db import DB
from noirwrit.memory.store import Memory
from noirwrit.planner import consistency
from noirwrit.planner.bible import Bible
from noirwrit.planner.generators import Generator
from noirwrit.planner.outline import Beat, Outline, plan
from noirwrit.planner.spec import Spec, fill

PROMPT_BUDGET_TOKENS = 1100  # leaves room in a 2048 window for ~900 new tokens per scene
MAX_SCENE_TRIES = 3
LIVE_INTERVAL_S = 0.1
CHUNK_TOKENS = 140  # best-of-N works on chunks this long

Progress = Callable[[dict], None] | None


@dataclass
class SceneResult:
    text: str
    tokens: int
    seconds: float
    tries: int
    issues: str


def used_names(db: DB) -> set[str]:
    return {r["name"] for r in db.query("SELECT DISTINCT name FROM names_used")}


def create_story(db: DB, spec: Spec, raw_request: str = "", parent_story_id: int | None = None) -> int:
    spec = fill(spec, used_names(db))
    spec_id = db.add_spec(json.loads(spec.to_json()), raw_request)
    outline = plan(spec, used_names(db))
    sid = db.execute(
        "INSERT INTO stories(created, spec_id, title, status, outline, parent_story_id) VALUES (?, ?, ?, 'planned', ?, ?)",
        (time.time(), spec_id, outline.title, json.dumps(outline.to_dict()), parent_story_id),
    ).lastrowid
    for ch in outline.chapters:
        db.execute("INSERT INTO chapters(story_id, num, title, status) VALUES (?, ?, ?, 'pending')", (sid, ch["num"], ch["title"]))
        for b in ch["beats"]:
            db.execute("INSERT INTO scenes(story_id, chapter_num, num, beat, status) VALUES (?, ?, ?, ?, 'pending')",
                       (sid, b.chapter, b.num, json.dumps(b.__dict__)))
    for c in outline.cast:
        db.execute("INSERT INTO names_used(story_id, name, role) VALUES (?, ?, ?)", (sid, c.name, c.role))
    db.execute("INSERT INTO themes(story_id, theme) VALUES (?, ?)", (sid, spec.motive))
    db.execute("INSERT INTO twists(story_id, twist) VALUES (?, ?)", (sid, spec.twist))
    Bible.from_outline(sid, outline).save(db)
    return int(sid)


def load_story(db: DB, story_id: int) -> tuple[dict, Spec, Outline]:
    row = db.one("SELECT s.*, p.data AS spec FROM stories s JOIN specs p ON p.id = s.spec_id WHERE s.id=?", (story_id,))
    if row is None:
        raise KeyError(f"story {story_id} not found")
    return dict(row), Spec.from_dict(json.loads(row["spec"])), Outline.from_dict(json.loads(row["outline"]))


def summarize_chapter(outline: Outline, chapter: int, text: str, max_words: int = 110) -> str:
    """~150-token rolling summary. Built from the planner's beats (reliable) plus the chapter's opening line."""
    ch = outline.chapters[chapter - 1]
    parts = [b.summary for b in ch["beats"]]
    s = f"Chapter {chapter}, {ch['title']}: " + " ".join(parts)
    words = s.split()
    return " ".join(words[:max_words])


def _tail(text: str, words: int) -> str:
    w = text.split()
    return " ".join(w[-words:])


def _trim_to_sentence(text: str) -> str:
    m = list(re.finditer(r'[.!?]["\']?(\s|$)', text))
    return text[: m[-1].end()].strip() if m else text.strip()


HEADING_RE = re.compile(r"^(chapter|book|part|volume|section)\b[\s\w.,:-]{0,60}$|^(the end|finis)\.?$", re.I)


def _is_heading(para: str) -> bool:
    """Book furniture the model copies from its training books: 'CHAPTER III.', 'THE SUPPERING GAME.'"""
    p = para.strip()
    if HEADING_RE.match(p):
        return True
    words = p.split()
    letters = [c for c in p if c.isalpha()]
    return 0 < len(words) <= 10 and bool(letters) and all(c.isupper() for c in letters) and not p.startswith('"')


def _tidy(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    # Strip any leaked control tokens.
    text = re.sub(r"<(pad|bos|eos|spec|beat|summary|bible|chapter|scene)>", "", text)
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n(?=[A-Z\"])", text)]
    text = "\n\n".join(p for p in paras if p and not _is_heading(p))
    return text.strip()


class StoryEngine:
    def __init__(self, db: DB, memory: Memory, generator: Generator, novelty_retries: int = 1, candidates: int = 1):
        self.db = db
        self.mem = memory
        self.gen = generator
        self.novelty_retries = novelty_retries
        # Best-of-N per chunk: 1 = stream every token; 2 or 3 = write in chunks and keep the best.
        self.candidates = max(1, candidates)
        self._scorer = None
        self._scorer_tried = False

    def scorer(self):
        """PyTorch scorer for the model in use, loaded once. None when no matching checkpoint exists."""
        if not self._scorer_tried:
            self._scorer_tried = True
            from noirwrit.runtime.score import ModelScorer, find_scorer_ckpt

            path = getattr(self.gen, "gguf", None) or getattr(self.gen, "ckpt", None)
            ck = find_scorer_ckpt(path) if path else None
            if ck:
                try:
                    self._scorer = ModelScorer(ck)
                except Exception:
                    self._scorer = None
        return self._scorer

    def _best_of(self, prompt: str, body: str, want: int, seed: int, on_token=None) -> tuple[str, int]:
        """Generate `candidates` continuations of prompt + body and return the best one, cut at a sentence end."""
        from noirwrit.runtime.score import combined

        context = _tail(f"{prompt} {body}".strip(), int(PROMPT_BUDGET_TOKENS / 1.3) + 200)
        best, best_score, used = "", -1e9, 0
        for c in range(self.candidates):
            raw, toks = self.gen.generate(context, want, seed=seed + 7919 * c, on_token=on_token)
            used += toks
            cand = _trim_to_sentence(raw) or raw.strip()
            if not cand:
                continue
            sc = self.scorer()
            lp = sc.mean_logprob(context, cand) if sc else None
            score = combined(lp, cand)
            if score > best_score:
                best, best_score = cand, score
        return best, used

    def build_prompt(self, spec: Spec, outline: Outline, bible: Bible, beat: Beat, prev_text: str,
                     prev_summary: str, story_id: int) -> str:
        header = f"{outline.title}. A {spec.genre.replace('_', ' ')} story, {spec.tone}, set in {spec.setting}, {spec.era}."
        hits = self.mem.search(beat.summary, k=3, story_id=story_id)
        retrieved = " ".join(h.text[:600] for h in hits if h.score > 0.2)
        parts = [header]
        if prev_summary:
            parts.append(prev_summary)
        if retrieved:
            parts.append(retrieved)
        parts.append(bible.slice_for(beat))
        # Budget: keep the newest material. Roughly 1.3 tokens per word.
        budget_words = int(PROMPT_BUDGET_TOKENS / 1.3)
        tail = _tail(prev_text, min(250, budget_words // 3))
        ctx = " ".join(parts)
        room = budget_words - len(tail.split()) - len(beat.lead.split()) - 10
        ctx = _tail(ctx, max(room, 50))
        return f"{ctx}\n\n{tail}\n\n{beat.lead}".strip() if tail else f"{ctx}\n\n{beat.lead}"

    def write_scene(self, spec, outline, bible, beat, prev_text, prev_summary, story_id, seed, on_token=None,
                    on_live=None) -> SceneResult:
        """on_token gets raw pieces; on_live gets the cleaned scene text so far, about 10 times a second."""
        t0 = time.time()
        issues = ""
        text, toks = "", 0
        for attempt in range(1, MAX_SCENE_TRIES + 1):
            prompt = self.build_prompt(spec, outline, bible, beat, prev_text, prev_summary, story_id)
            max_new = int(beat.target_words * 1.35)
            buf = [beat.lead, " "]
            last = [0.0]

            def tok(piece: str, buf=buf, last=last) -> None:
                buf.append(piece)
                if on_token:
                    on_token(piece)
                now = time.time()
                if on_live and now - last[0] >= LIVE_INTERVAL_S:
                    last[0] = now
                    on_live(consistency.check(_tidy("".join(buf)), bible, beat).fixed_text)

            if on_live:
                on_live(beat.lead)  # a retry restarts the scene from its lead-in
            if self.candidates == 1:
                raw, toks = self.gen.generate(prompt, max_new, seed=seed * 101 + attempt, on_token=tok)
            else:
                # Chunked best-of-N. Only chosen text is published to the live stream.
                body, toks, k = "", 0, 0
                while toks < max_new:
                    want = min(CHUNK_TOKENS, max_new - toks)
                    piece, used = self._best_of(prompt + "\n\n" + beat.lead, body, want,
                                                seed * 101 + attempt * 1009 + k * 31, on_token)
                    toks += max(used // self.candidates, 1)
                    k += 1
                    if not piece:
                        break
                    body = f"{body} {piece}".strip()
                    if on_live:
                        on_live(consistency.check(_tidy(beat.lead + " " + body), bible, beat).fixed_text)
                raw = body
            text = _tidy(beat.lead + " " + _trim_to_sentence(raw))
            rep = consistency.check(text, bible, beat)
            text = rep.fixed_text
            issues = rep.summary()
            if not rep.needs_regenerate:
                return SceneResult(text, toks, time.time() - t0, attempt, issues)
        return SceneResult(text, toks, time.time() - t0, MAX_SCENE_TRIES, issues + " (kept after retries)")

    def write_chapter(self, story_id: int, chapter: int, progress: Progress = None,
                      should_stop: Callable[[], bool] | None = None, between_scenes: Callable[[], None] | None = None) -> str:
        info, spec, outline = load_story(self.db, story_id)
        bible = Bible.load(self.db, story_id) or Bible.from_outline(story_id, outline)
        beats = outline.chapters[chapter - 1]["beats"]
        prev_summary = ""
        if chapter > 1:
            r = self.db.one("SELECT text FROM summaries WHERE story_id=? AND chapter_num=?", (story_id, chapter - 1))
            prev_summary = r["text"] if r else ""
        self.db.execute("UPDATE chapters SET status='writing', updated=? WHERE story_id=? AND num=?", (time.time(), story_id, chapter))
        self.db.execute("UPDATE stories SET status='writing' WHERE id=?", (story_id,))

        texts = []
        prev_text = ""
        if chapter > 1:
            r = self.db.one("SELECT text FROM chapters WHERE story_id=? AND num=?", (story_id, chapter - 1))
            prev_text = (r["text"] or "") if r else ""
        for beat in beats:
            row = self.db.one("SELECT status, text FROM scenes WHERE story_id=? AND chapter_num=? AND num=?",
                              (story_id, chapter, beat.num))
            if row and row["status"] == "done":
                texts.append(row["text"])
                prev_text = row["text"]
                continue
            if should_stop and should_stop():
                raise InterruptedError("stop requested")
            if between_scenes:
                between_scenes()
            if progress:
                progress({"event": "scene_start", "chapter": chapter, "scene": beat.num, "of": len(beats),
                          "target_tokens": int(beat.target_words * 1.35)})

            def on_tok(piece: str, b=beat) -> None:
                if progress:
                    progress({"event": "token", "chapter": chapter, "scene": b.num, "text": piece})

            def on_live(text: str, b=beat) -> None:
                if progress:
                    progress({"event": "scene_live", "chapter": chapter, "scene": b.num, "text": text})

            res = self.write_scene(spec, outline, bible, beat, prev_text, prev_summary, story_id,
                                   seed=spec.seed * 1000 + chapter * 50 + beat.num, on_token=on_tok, on_live=on_live)
            bible.update_after_scene(beat, res.text)
            bible.save(self.db)
            self.db.execute(
                "UPDATE scenes SET status='done', text=?, tokens=?, seconds=? WHERE story_id=? AND chapter_num=? AND num=?",
                (res.text, res.tokens, res.seconds, story_id, chapter, beat.num),
            )
            self.mem.ingest_text(res.text, source=f"story{story_id}/ch{chapter}/sc{beat.num}", story_id=story_id, kind="scene")
            texts.append(res.text)
            prev_text = res.text
            if progress:
                progress({"event": "scene_done", "chapter": chapter, "scene": beat.num, "of": len(beats),
                          "tokens": res.tokens, "seconds": round(res.seconds, 2), "issues": res.issues})

        chapter_text = "\n\n".join(texts)
        nov = self.mem.novelty(chapter_text, story_id=story_id)
        summary = summarize_chapter(outline, chapter, chapter_text)
        self.db.execute(
            "INSERT INTO summaries(story_id, chapter_num, text) VALUES (?, ?, ?) "
            "ON CONFLICT(story_id, chapter_num) DO UPDATE SET text=excluded.text",
            (story_id, chapter, summary),
        )
        self.db.execute("UPDATE chapters SET status='done', text=?, words=?, updated=? WHERE story_id=? AND num=?",
                        (chapter_text, len(chapter_text.split()), time.time(), story_id, chapter))
        done = self.db.one("SELECT COUNT(*) AS n FROM chapters WHERE story_id=? AND status!='done'", (story_id,))["n"]
        self.db.execute("UPDATE stories SET status=? WHERE id=?", ("done" if done == 0 else "writing", story_id))
        if progress:
            progress({"event": "chapter_done", "chapter": chapter, "words": len(chapter_text.split()),
                      "novel": nov.novel, "max_cosine": round(nov.max_cosine, 3), "ngram_overlap": round(nov.ngram_overlap, 3)})
        return chapter_text

    def write_story(self, story_id: int, progress: Progress = None) -> list[str]:
        n = self.db.one("SELECT COUNT(*) AS n FROM chapters WHERE story_id=?", (story_id,))["n"]
        return [self.write_chapter(story_id, c, progress) for c in range(1, n + 1)]
