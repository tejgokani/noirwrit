#!/usr/bin/env python3
"""Measure ETA accuracy with a real model: calibrate on chapter 1, predict and time chapters 2..N.

    python tools/eta_check.py --model artifacts/tiny/export/noirwrit-tiny-q8_0.gguf

Appends the result to docs/BENCH.md.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from noirwrit.memory.db import DB  # noqa: E402
from noirwrit.memory.embed import HashingEmbedder  # noqa: E402
from noirwrit.memory.store import Memory  # noqa: E402
from noirwrit.planner.generators import LlamaCppGenerator, TorchGenerator  # noqa: E402
from noirwrit.planner.spec import Spec  # noqa: E402
from noirwrit.planner.story import StoryEngine, create_story  # noqa: E402
from noirwrit.worker import Worker, enqueue_chapter, eta_seconds  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--chapters", type=int, default=4)
    ap.add_argument("--words", type=int, default=3000)
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        db = DB(Path(tmp) / "eta.db")
        gen = LlamaCppGenerator(a.model) if a.model.endswith(".gguf") else TorchGenerator(a.model)
        eng = StoryEngine(db, Memory(db, HashingEmbedder()), gen)
        sid = create_story(db, Spec(seed=77, chapters=a.chapters, chapter_words=a.words))
        rows = []
        for ch in range(1, a.chapters + 1):
            predicted = eta_seconds(db, sid, ch)
            enqueue_chapter(db, sid, ch)
            w = Worker(db, lambda _db: eng, prefetch=False)
            t0 = time.time()
            w.run(once=True)
            actual = time.time() - t0
            rows.append((ch, predicted, actual))
            p = "n/a (calibrating)" if predicted is None else f"{predicted:.1f} s"
            err = "" if predicted is None else f"{abs(predicted - actual) / actual:.0%}"
            print(f"chapter {ch}: predicted {p}, actual {actual:.1f} s {err}", flush=True)
    errs = [abs(p - t) / t for _, p, t in rows if p is not None]
    worst = max(errs) if errs else float("nan")
    lines = ["", "## ETA accuracy", "",
             f"Model: `{Path(a.model).name}`, {a.chapters} chapters of {a.words} words. The rolling tok/s is calibrated on chapter 1.", "",
             "| Chapter | Predicted | Actual | Error |", "|---|---|---|---|"]
    for ch, p, t in rows:
        lines.append(f"| {ch} | {'calibrating' if p is None else f'{p:.1f} s'} | {t:.1f} s | {'' if p is None else f'{abs(p - t) / t:.0%}'} |")
    lines.append(f"\nWorst error after calibration: **{worst:.0%}** (target under 20%: {'pass' if worst < 0.2 else 'FAIL'}).")
    bench = ROOT / "docs" / "BENCH.md"
    text = bench.read_text() if bench.exists() else "# Benchmarks\n"
    if "## ETA accuracy" in text:
        text = text[: text.index("\n## ETA accuracy")]
    bench.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n")
    print(f"worst error {worst:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
