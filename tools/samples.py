#!/usr/bin/env python3
"""Write sample stories with a real model and save them to docs/samples/.

    python tools/samples.py --model artifacts/base/export/noirwrit-base-q8_0.gguf --stories 5 --chapters 1
    python tools/samples.py --model artifacts/tiny/latest.pt --stories 1 --chapters 5 --words 600 --out artifacts/samples-tiny

Uses a throwaway database so samples never touch the user's library.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from noirwrit.memory.db import DB  # noqa: E402
from noirwrit.memory.embed import get_embedder  # noqa: E402
from noirwrit.memory.store import Memory  # noqa: E402
from noirwrit.planner.generators import LlamaCppGenerator, TorchGenerator  # noqa: E402
from noirwrit.planner.spec import Spec  # noqa: E402
from noirwrit.planner.story import StoryEngine, create_story  # noqa: E402

GENRES = ["noir", "noir", "classic_detective", "thriller", "noir"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--stories", type=int, default=5)
    ap.add_argument("--chapters", type=int, default=1)
    ap.add_argument("--words", type=int, default=3000)
    ap.add_argument("--out", default=str(ROOT / "docs" / "samples"))
    ap.add_argument("--seed", type=int, default=100)
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    db_path = out / "samples.db"
    db_path.unlink(missing_ok=True)
    db = DB(db_path)
    mem = Memory(db, get_embedder())
    gen = LlamaCppGenerator(a.model) if a.model.endswith(".gguf") else TorchGenerator(a.model, int8=False)
    eng = StoryEngine(db, mem, gen)

    index = ["# Sample chapters", "", f"Model: `{Path(a.model).name}`. Generated {time.strftime('%Y-%m-%d')} on this Mac, offline.", ""]
    for i in range(a.stories):
        spec = Spec(chapters=a.chapters, genre=GENRES[i % len(GENRES)], chapter_words=a.words, seed=a.seed + i)
        sid = create_story(db, spec)
        title = db.one("SELECT title FROM stories WHERE id=?", (sid,))["title"]
        t0 = time.time()
        issues = []
        texts = eng.write_story(sid, progress=lambda ev, acc=issues: acc.append(ev.get("issues")) if ev["event"] == "scene_done" else None)
        secs = time.time() - t0
        words = sum(len(t.split()) for t in texts)
        fname = f"{i + 1:02d}-{title.lower().replace(' ', '-').replace(chr(39), '')}.md"
        rows = db.query("SELECT num, title, text FROM chapters WHERE story_id=? ORDER BY num", (sid,))
        body = [f"# {title}", "", f"*{spec.genre.replace('_', ' ')}, seed {spec.seed}. {words} words in {secs:.0f} s.*", ""]
        for r in rows:
            body += [f"## Chapter {r['num']}: {r['title']}", "", r["text"], ""]
        (out / fname).write_text("\n".join(body))
        fixes = [x for x in issues if x and x != "ok"]
        index.append(f"- [{title}]({fname}): {spec.genre.replace('_', ' ')}, {a.chapters} chapter(s), {words} words, "
                     f"{secs:.0f} s, consistency fixes: {len(fixes)}")
        print(json.dumps({"story": sid, "title": title, "words": words, "seconds": round(secs, 1),
                          "fixes": fixes[:5]}), flush=True)
    (out / "README.md").write_text("\n".join(index) + "\n")
    for p in (db_path, db_path.with_name(db_path.name + "-wal"), db_path.with_name(db_path.name + "-shm")):
        p.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
