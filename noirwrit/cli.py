"""noirwrit command line entry point."""

from __future__ import annotations

import argparse
import json
import sys

from noirwrit import __version__


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="noirwrit", description="Offline crime and noir chapter generator.")
    p.add_argument("--version", action="version", version=f"noirwrit {__version__}")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("serve", help="run the local web app")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8765)
    s.add_argument("--no-browser", action="store_true")

    sub.add_parser("worker", help="run the background generation worker")
    sub.add_parser("info", help="show config, models and paths")

    n = sub.add_parser("new", help="plan and write a story from the terminal")
    n.add_argument("--chapters", type=int, default=3)
    n.add_argument("--genre", default="noir")
    n.add_argument("--words", type=int, default=3000)
    n.add_argument("--seed", type=int, default=0)

    d = sub.add_parser("demo", help="write a short story with the installed model and export PDF and EPUB")
    d.add_argument("--out", default="noirwrit-demo")
    d.add_argument("--chapters", type=int, default=1)
    d.add_argument("--words", type=int, default=1500)

    im = sub.add_parser("install-model", help="install a GGUF model into ~/.noirwrit/models")
    im.add_argument("source", nargs="?", default="",
                    help="a local .gguf file, or a Hugging Face repo id; default: this checkout's trained base model")

    e = sub.add_parser("export", help="export a story")
    e.add_argument("story_id", type=int)
    e.add_argument("--fmt", default="pdf", choices=["pdf", "epub", "txt", "md"])
    e.add_argument("--page-size", default="6x9", choices=["A4", "Letter", "A5", "6x9"])
    e.add_argument("--out", default="")

    a = p.parse_args(argv)
    if a.cmd == "serve":
        from noirwrit.app.server import serve

        serve(a.host, a.port, open_browser=not a.no_browser)
        return 0
    if a.cmd == "worker":
        from noirwrit.worker import main as worker_main

        return worker_main([])
    if a.cmd == "info":
        from noirwrit.config import HOME, load_requirements
        from noirwrit.runtime.models import list_models

        print(json.dumps({"version": __version__, "home": str(HOME), "models": list_models(),
                          "requirements": load_requirements()}, indent=2))
        return 0
    if a.cmd == "new":
        from noirwrit.config import HOME
        from noirwrit.memory.db import DB
        from noirwrit.memory.store import Memory
        from noirwrit.planner.spec import Spec
        from noirwrit.planner.story import StoryEngine, create_story
        from noirwrit.runtime.models import load_generator

        db = DB(HOME / "noirwrit.db")
        sid = create_story(db, Spec(chapters=a.chapters, genre=a.genre, chapter_words=a.words, seed=a.seed))
        eng = StoryEngine(db, Memory(db), load_generator(db))
        print(f"story {sid}: {db.one('SELECT title FROM stories WHERE id=?', (sid,))['title']}", flush=True)

        def show(ev: dict) -> None:
            if ev["event"] == "token":
                sys.stdout.write(ev["text"])
                sys.stdout.flush()
            elif ev["event"] == "scene_start":
                print(f"\n\n[chapter {ev['chapter']}, scene {ev['scene']}/{ev['of']}]\n", flush=True)

        eng.write_story(sid, progress=show)
        print(f"\n\ndone: story {sid}")
        return 0
    if a.cmd == "install-model":
        from noirwrit.runtime.models import install_model

        print(install_model(a.source))
        return 0
    if a.cmd == "demo":
        return demo(a.out, a.chapters, a.words)
    if a.cmd == "export":
        from pathlib import Path

        from noirwrit.config import HOME
        from noirwrit.export import books as ex
        from noirwrit.memory.db import DB

        db = DB(HOME / "noirwrit.db")
        st = db.one("SELECT title FROM stories WHERE id=?", (a.story_id,))
        rows = db.query("SELECT title, text FROM chapters WHERE story_id=? AND status='done' ORDER BY num", (a.story_id,))
        if not st or not rows:
            print("no finished chapters for that story", file=sys.stderr)
            return 1
        book = ex.Book(st["title"], [(r["title"], r["text"]) for r in rows])
        out = Path(a.out or f"{st['title'].replace(' ', '_')}.{a.fmt}")
        opts = ex.ExportOptions(page_size=a.page_size)
        if a.fmt == "pdf":
            ex.to_pdf(book, out, opts)
        elif a.fmt == "epub":
            ex.to_epub(book, out, opts)
        else:
            out.write_text(ex.to_txt(book) if a.fmt == "txt" else ex.to_md(book))
        print(out)
        return 0
    p.print_help()
    return 0


def demo(out_dir: str, chapters: int, words: int) -> int:
    """End-to-end check for a fresh install: plan, write, export. Uses a throwaway database."""
    import tempfile
    import time
    from pathlib import Path

    from noirwrit.export import books as ex
    from noirwrit.memory.db import DB
    from noirwrit.memory.store import Memory
    from noirwrit.planner.spec import Spec
    from noirwrit.planner.story import StoryEngine, create_story
    from noirwrit.runtime.models import load_generator, pick_model

    pick = pick_model()
    print(f"model: {pick['path'] if pick else 'none installed (run: noirwrit install-model); using the stand-in generator'}")
    with tempfile.TemporaryDirectory() as tmp:
        db = DB(Path(tmp) / "demo.db")
        eng = StoryEngine(db, Memory(db), load_generator(db))
        sid = create_story(db, Spec(chapters=chapters, chapter_words=words, seed=int(time.time()) % 10000))
        title = db.one("SELECT title FROM stories WHERE id=?", (sid,))["title"]
        print(f"writing \"{title}\"...", flush=True)
        t0 = time.time()

        def show(ev: dict) -> None:
            if ev["event"] == "scene_done":
                print(f"  chapter {ev['chapter']}, scene {ev['scene']}/{ev['of']} ({ev['tokens']} tokens)", flush=True)

        eng.write_story(sid, progress=show)
        rows = db.query("SELECT title, text FROM chapters WHERE story_id=? ORDER BY num", (sid,))
        book = ex.Book(title, [(r["title"], r["text"]) for r in rows])
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        pdf = ex.to_pdf(book, out / "demo.pdf")
        epub = ex.to_epub(book, out / "demo.epub")
        (out / "demo.md").write_text(ex.to_md(book))
    words_out = sum(len(r["text"].split()) for r in rows)
    print(f"done: {words_out} words in {time.time() - t0:.0f} s -> {pdf}, {epub}, {out / 'demo.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
