"""Train the 16k byte-level BPE tokenizer and pack the corpus into uint16 shards.

Usage:
    python -m noirwrit.tokenizer.train_tokenizer           # train + pack
    python -m noirwrit.tokenizer.train_tokenizer --pack-only
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Cap Rust thread pools at 4 of 8 cores (Mac safety rule for data prep).
os.environ.setdefault("RAYON_NUM_THREADS", "4")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")

import numpy as np  # noqa: E402
from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers  # noqa: E402

from noirwrit.config import PACKAGE, ROOT  # noqa: E402

VOCAB_SIZE = 16384
SPECIAL_TOKENS = ["<pad>", "<bos>", "<eos>", "<spec>", "<beat>", "<summary>", "<bible>", "<chapter>", "<scene>"]
TOKENIZER_PATH = PACKAGE / "tokenizer" / "noirwrit-16k.json"
CLEAN = ROOT / "data" / "clean"
SHARDS = ROOT / "data" / "shards"
SETS = ("general", "crime", "noir")
VAL_SHARE = 0.02


def book_files() -> list[Path]:
    return sorted(CLEAN.glob("*/*.txt"))


def train(files: list[Path], vocab_size: int = VOCAB_SIZE) -> Tokenizer:
    tok = Tokenizer(models.BPE(unk_token=None, byte_fallback=False))
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=True)
    tok.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        min_frequency=2,
        special_tokens=SPECIAL_TOKENS,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        show_progress=False,
    )
    tok.train([str(f) for f in files], trainer)
    return tok


def load_tokenizer(path: Path = TOKENIZER_PATH) -> Tokenizer:
    return Tokenizer.from_file(str(path))


def pack(tok: Tokenizer, batch: int = 32) -> dict:
    """Write data/shards/{set}_{train,val}.bin as uint16, books separated by <eos>.

    The last VAL_SHARE of every book goes to val. That gives every set (even the
    small noir set) a validation slice that covers all its authors, and the
    val text itself never appears in train.
    """
    SHARDS.mkdir(parents=True, exist_ok=True)
    eos = tok.token_to_id("<eos>")
    counts: dict[str, dict[str, int]] = {}
    for s in SETS:
        files = sorted((CLEAN / s).glob("*.txt"))
        counts[s] = {"train": 0, "val": 0, "books": len(files)}
        outs = {split: (SHARDS / f"{s}_{split}.bin").open("wb") for split in ("train", "val")}
        try:
            for i in range(0, len(files), batch):
                chunk = files[i:i + batch]
                encs = tok.encode_batch([f.read_text() for f in chunk])
                for e in encs:
                    ids = e.ids
                    cut = int(len(ids) * (1 - VAL_SHARE))
                    tr = np.array([*ids[:cut], eos], dtype=np.uint16)
                    va = np.array([*ids[cut:], eos], dtype=np.uint16)
                    outs["train"].write(tr.tobytes())
                    outs["val"].write(va.tobytes())
                    counts[s]["train"] += len(tr)
                    counts[s]["val"] += len(va)
        finally:
            for fh in outs.values():
                fh.close()
    (SHARDS / "meta.json").write_text(json.dumps({"vocab_size": tok.get_vocab_size(), "eos": eos, "counts": counts}, indent=2))
    return counts


def eval_tokenizer(tok: Tokenizer, files: list[Path], sample_chars: int = 2_000_000) -> dict:
    """Round-trip check and tokens per word on a sample of the corpus."""
    text_parts, total = [], 0
    step = max(len(files) // 50, 1)
    for f in files[::step]:
        t = f.read_text()[:100_000]
        text_parts.append(t)
        total += len(t)
        if total >= sample_chars:
            break
    mismatches = 0
    tokens = words = 0
    for t in text_parts:
        ids = tok.encode(t).ids
        if tok.decode(ids, skip_special_tokens=False) != t:
            mismatches += 1
        tokens += len(ids)
        words += len(t.split())
    return {"docs": len(text_parts), "roundtrip_mismatches": mismatches, "tokens_per_word": tokens / max(words, 1)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args(argv)
    files = book_files()
    if not files:
        print("no cleaned books in data/clean; run python -m noirwrit.corpus.build first", file=sys.stderr)
        return 1
    if a.pack_only:
        tok = load_tokenizer()
    else:
        print(f"training BPE {VOCAB_SIZE} on {len(files)} books", flush=True)
        tok = train(files)
        TOKENIZER_PATH.parent.mkdir(parents=True, exist_ok=True)
        tok.save(str(TOKENIZER_PATH))
    ev = eval_tokenizer(tok, files)
    print(json.dumps(ev, indent=2))
    counts = pack(tok)
    print(json.dumps(counts, indent=2))

    # Fill exact token counts into data/STATS.md.
    stats_path = ROOT / "data" / "stats.json"
    if stats_path.exists():
        from noirwrit.corpus.build import write_stats

        stats = json.loads(stats_path.read_text())["sets"]
        write_stats(stats, {s: c["train"] + c["val"] for s, c in counts.items()})
    (ROOT / "data" / "tokenizer_eval.json").write_text(json.dumps(ev, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
