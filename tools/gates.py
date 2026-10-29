#!/usr/bin/env python3
"""Check the plan.md section 6 export and novelty gates with the trained model. Writes docs/GATES.md.

    python tools/guard.py --timeout-min 15 -- python tools/gates.py

- PDF: a 12-chapter story in A4, Letter, A5 and 6x9 with a table of contents (page numbers that
  match the chapter openers), running headers, page numbers, and no text outside the page box.
- EPUB: the same story passes epubcheck.
- Novelty: two stories from the same prompt differ (embedding cosine below 0.85 and low 5-gram overlap).
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from noirwrit.export import books as ex  # noqa: E402
from noirwrit.memory.db import DB  # noqa: E402
from noirwrit.memory.embed import get_embedder  # noqa: E402
from noirwrit.memory.store import NOVELTY_COSINE, Memory  # noqa: E402
from noirwrit.planner.generators import LlamaCppGenerator  # noqa: E402
from noirwrit.planner.spec import Spec  # noqa: E402
from noirwrit.planner.story import StoryEngine, create_story  # noqa: E402


def pdf_checks(pdf: Path, n_chapters: int, title: str) -> dict:
    from pypdf import PdfReader

    r = PdfReader(str(pdf))
    pages = [p.extract_text() or "" for p in r.pages]
    toc_page = next(i for i, t in enumerate(pages) if "CONTENTS" in t.upper())
    toc_nums = [int(x) for x in re.findall(r"\.{3,}\s*(\d+)", pages[toc_page])]
    openers = [i + 1 for i, t in enumerate(pages) if re.search(r"C\s*H\s*A\s*P\s*T\s*E\s*R\s+\d+", t)]
    numbered = sum(bool(re.search(rf"(^|\n)\s*{i + 1}\s*$", t.strip())) for i, t in enumerate(pages[toc_page + 1:], toc_page + 1))
    header = sum(title.split()[0] in t for t in pages[toc_page + 1:])
    # Text outside the page box would show up as glyphs placed beyond the media box.
    outside = 0
    for page in r.pages:
        w, h = float(page.mediabox.width), float(page.mediabox.height)

        def visitor(text, cm, tm, font, size, w=w, h=h):
            nonlocal outside
            x, y = tm[4] * cm[0] + cm[4], tm[5] * cm[3] + cm[5]
            if text.strip() and not (0 <= x <= w and 0 <= y <= h):
                outside += 1

        page.extract_text(visitor_text=visitor)
    return {"pages": len(pages), "toc_entries": len(toc_nums), "toc_matches_openers": toc_nums == openers[:len(toc_nums)],
            "chapter_openers": len(openers), "pages_with_numbers": numbered, "pages_with_header": header,
            "glyphs_outside_page": outside, "size_in": (round(float(r.pages[0].mediabox.width) / 72, 2),
                                                        round(float(r.pages[0].mediabox.height) / 72, 2))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=str(ROOT / "artifacts" / "base" / "export" / "noirwrit-base-q8_0.gguf"))
    ap.add_argument("--chapters", type=int, default=12)
    ap.add_argument("--words", type=int, default=1500)
    a = ap.parse_args()
    out = ROOT / "artifacts" / "gates"
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# Quality gates", "", f"Model: `{Path(a.model).name}`. Run {time.strftime('%Y-%m-%d')} on this Mac.", ""]
    ok_all = True

    with tempfile.TemporaryDirectory() as tmp:
        db = DB(Path(tmp) / "g.db")
        mem = Memory(db, get_embedder())
        eng = StoryEngine(db, mem, LlamaCppGenerator(a.model))

        # 1. Twelve-chapter book.
        t0 = time.time()
        sid = create_story(db, Spec(seed=2024, chapters=a.chapters, chapter_words=a.words, genre="noir"))
        texts = eng.write_story(sid)
        title = db.one("SELECT title FROM stories WHERE id=?", (sid,))["title"]
        rows = db.query("SELECT title, text FROM chapters WHERE story_id=? ORDER BY num", (sid,))
        book = ex.Book(title, [(r["title"], r["text"]) for r in rows])
        words = sum(len(t.split()) for t in texts)
        lines += [f"## {a.chapters}-chapter book", "", f"\"{title}\": {words:,} words written in {time.time() - t0:.0f} s.", "",
                  "| Page size | Pages | TOC entries | TOC page numbers match chapter openers | Pages with page numbers | Pages with running header | Glyphs outside the page |",
                  "|---|---|---|---|---|---|---|"]
        for size in ("A4", "Letter", "A5", "6x9"):
            pdf = ex.to_pdf(book, out / f"book-{size}.pdf", ex.ExportOptions(page_size=size))
            c = pdf_checks(pdf, a.chapters, title)
            good = c["toc_entries"] == a.chapters and c["toc_matches_openers"] and c["glyphs_outside_page"] == 0 \
                and c["pages_with_numbers"] >= c["pages"] - 4
            ok_all &= good
            lines.append(f"| {size} ({c['size_in'][0]} x {c['size_in'][1]} in) | {c['pages']} | {c['toc_entries']} | "
                         f"{'yes' if c['toc_matches_openers'] else 'NO'} | {c['pages_with_numbers']} | {c['pages_with_header']} | "
                         f"{c['glyphs_outside_page']} |")
            print(size, c, flush=True)

        epub = ex.to_epub(book, out / "book.epub")
        res = ex.epubcheck(epub)
        if res is None:
            lines += ["", "EPUB: epubcheck not installed, not validated."]
            ok_all = False
        else:
            ok, log = res
            ok_all &= ok
            summary = next((ln for ln in log.splitlines() if "fatal" in ln.lower() and "error" in ln.lower()), log.strip().splitlines()[-1])
            lines += ["", f"EPUB: epubcheck {'passed' if ok else 'FAILED'} ({summary.strip()})."]
            print("epubcheck:", ok, summary, flush=True)
            if not ok:
                print(log[-3000:])

        # 2. Novelty: the same prompt twice.
        spec = {"chapters": 1, "chapter_words": 1500, "genre": "noir", "setting": "a fog-bound port city", "victim": "a pawnbroker"}
        a_id = create_story(db, Spec(seed=1, **spec))
        b_id = create_story(db, Spec(seed=2, **spec))
        ta = eng.write_chapter(a_id, 1)
        tb = eng.write_chapter(b_id, 1)
        rep = mem.novelty(tb, story_id=b_id)
        cos_ab = float(mem.emb.embed_one(ta) @ mem.emb.embed_one(tb))
        novel = rep.max_cosine < NOVELTY_COSINE and rep.ngram_overlap < 0.25
        ok_all &= novel
        lines += ["", "## Novelty", "",
                  f"Two stories from the same prompt ({spec['setting']}, victim {spec['victim']}): whole-chapter cosine {cos_ab:.2f}, "
                  f"closest-passage cosine {rep.max_cosine:.2f} (threshold {NOVELTY_COSINE}), 5-gram overlap {rep.ngram_overlap:.1%}, "
                  f"embedder `{mem.emb.name}`. {'Pass' if novel else 'FAIL'}."]
        print("novelty:", rep, flush=True)

    lines += ["", f"**Overall: {'all gates pass' if ok_all else 'some gates FAIL'}.**",
              "", "PDFs and the EPUB are in `artifacts/gates/` (not committed)."]
    (ROOT / "docs" / "GATES.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
