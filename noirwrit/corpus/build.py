"""Build the cleaned corpus: select, fetch, verify PD, clean, dedupe, split, report.

Usage:
    python -m noirwrit.corpus.build [--workers 4] [--limit N]

Outputs:
    data/clean/{general,crime,noir}/<id>.txt   cleaned books (gitignored)
    data/manifest.jsonl                       one row per kept book
    data/SOURCES.md                           per-title source and PD basis
    data/STATS.md                             counts and the language sanity rate
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from noirwrit.config import ROOT
from noirwrit.corpus.catalog import PD_CUTOFF, Book, load_catalog, select
from noirwrit.corpus.clean import (
    clean_text,
    front_matter_years,
    header_says_copyrighted,
    paragraph_passes,
    strip_gutenberg,
)
from noirwrit.corpus.fetch import fetch_book

DATA = ROOT / "data"
SETS = ("general", "crime", "noir")
MIN_WORDS = 3000
MIN_BOOK_PASS_RATE = 0.97


@dataclass
class Result:
    book: Book
    status: str  # kept | dropped
    reason: str = ""
    text: str = ""
    words: int = 0
    paras: int = 0
    paras_ok: int = 0


def process(book: Book, raw_dir: Path) -> Result:
    raw = fetch_book(book.id, raw_dir)
    if raw is None:
        return Result(book, "dropped", "download failed")
    header, body = strip_gutenberg(raw)
    if header_says_copyrighted(header):
        return Result(book, "dropped", "PG marks it copyrighted")
    years = [y for y in front_matter_years(body, header) if 1800 <= y <= 2030]
    late = [y for y in years if y > PD_CUTOFF]
    if late:
        return Result(book, "dropped", f"front matter has year {max(late)} (unsure, left out)")
    if not book.pd_basis:
        if not years:
            return Result(book, "dropped", "no dated front matter and contributor alive after 1930")
        book.pd_basis = f"front matter dated {max(years)}"
        book.year = max(years)
    text = clean_text(body)
    paras = [p for p in text.split("\n\n") if p.strip()]
    ok = sum(paragraph_passes(p) for p in paras)
    words = len(text.split())
    if words < MIN_WORDS:
        return Result(book, "dropped", f"too short ({words} words)")
    rate = ok / max(len(paras), 1)
    if rate < MIN_BOOK_PASS_RATE:
        return Result(book, "dropped", f"language sanity {rate:.2%}")
    # Drop paragraphs that fail the sanity check so the kept text passes cleanly.
    text = "\n\n".join(p for p in paras if paragraph_passes(p)) + "\n"
    return Result(book, "kept", text=text, words=words, paras=len(paras), paras_ok=ok)


def shingles(text: str, n: int = 8, keep_mod: int = 16) -> set[int]:
    """Sampled hashed word n-grams for near-duplicate detection."""
    words = re.findall(r"[a-z']+", text.lower())
    out = set()
    for i in range(0, max(len(words) - n + 1, 0)):
        h = int.from_bytes(hashlib.blake2b(" ".join(words[i:i + n]).encode(), digest_size=8).digest(), "big")
        if h % keep_mod == 0:
            out.add(h)
    return out


def dedupe(results: list[Result], threshold: float = 0.5) -> list[Result]:
    """Drop a book when most of its shingles already appear in a larger kept book."""
    kept: list[Result] = []
    index: dict[int, int] = {}
    for r in sorted(results, key=lambda x: -x.words):
        sh = shingles(r.text)
        if not sh:
            continue
        hits: dict[int, int] = defaultdict(int)
        for h in sh:
            if h in index:
                hits[index[h]] += 1
        if hits and max(hits.values()) / len(sh) >= threshold:
            other = kept[max(hits, key=hits.get)].book
            r.status, r.reason = "dropped", f"near duplicate of {other.id} ({other.title[:40]})"
            continue
        idx = len(kept)
        kept.append(r)
        for h in sh:
            index.setdefault(h, idx)
    return kept


def write_outputs(kept: list[Result], dropped: list[Result]) -> dict:
    clean_dir = DATA / "clean"
    for s in SETS:
        d = clean_dir / s
        d.mkdir(parents=True, exist_ok=True)
        # Start clean so books dropped by this run do not linger from an older run.
        for old in d.glob("*.txt"):
            old.unlink()
    stats = {s: {"books": 0, "words": 0, "paras": 0, "paras_ok": 0} for s in SETS}
    with (DATA / "manifest.jsonl").open("w") as mf:
        for r in sorted(kept, key=lambda x: (x.book.set, x.book.id)):
            b = r.book
            (clean_dir / b.set / f"{b.id}.txt").write_text(r.text)
            st = stats[b.set]
            st["books"] += 1
            st["words"] += r.words
            st["paras"] += r.paras
            st["paras_ok"] += r.paras_ok
            mf.write(json.dumps({
                "id": b.id, "set": b.set, "title": b.title, "author": b.author_line,
                "year": b.year, "pd_basis": b.pd_basis, "words": r.words,
            }) + "\n")

    lines = [
        "# Data sources",
        "",
        "All texts come from Project Gutenberg (gutenberg.org), which hosts works it has cleared as public domain in the United States.",
        f"Noirwrit applies a stricter rule on top: the work must be published in {PD_CUTOFF} or earlier. A title is kept only when one of these holds:",
        "",
        f"1. Every listed contributor (author, translator, editor) died in {PD_CUTOFF} or earlier.",
        f"2. The first publication year is well established and is {PD_CUTOFF} or earlier (listed in `noirwrit/corpus/catalog.py`, `KNOWN_YEARS`).",
        f"3. A pulp issue date in the title is {PD_CUTOFF} or earlier.",
        f"4. The book's own front matter carries a copyright or publication year, and the latest one is {PD_CUTOFF} or earlier.",
        "",
        f"Any book whose front matter mentions a year after {PD_CUTOFF} is left out, even when another rule passes. Unsure means out.",
        "",
        f"Kept: {len(kept)} books. Dropped: {len(dropped)} (reasons in `data/dropped.jsonl`).",
        "",
    ]
    for s in SETS:
        rows = [r for r in kept if r.book.set == s]
        lines += [f"## {s} ({len(rows)} books)", "", "| Gutenberg ID | Author | Title | Year | PD basis |", "|---|---|---|---|---|"]
        for r in sorted(rows, key=lambda x: (x.book.author_line, x.book.title)):
            b = r.book
            title = b.title.replace("|", "/")[:90]
            lines.append(f"| {b.id} | {b.author_line.replace('|', '/')[:50]} | {title} | {b.year or ''} | {b.pd_basis} |")
        lines.append("")
    (DATA / "SOURCES.md").write_text("\n".join(lines))

    with (DATA / "dropped.jsonl").open("w") as df:
        for r in dropped:
            df.write(json.dumps({"id": r.book.id, "set": r.book.set, "title": r.book.title, "reason": r.reason}) + "\n")
    return stats


def write_stats(stats: dict, token_counts: dict | None = None) -> None:
    total_p = sum(s["paras"] for s in stats.values())
    total_ok = sum(s["paras_ok"] for s in stats.values())
    lines = [
        "# Corpus stats",
        "",
        "| Set | Books | Words | Tokens | Paragraphs passing sanity filter |",
        "|---|---|---|---|---|",
    ]
    for s in SETS:
        st = stats[s]
        tok = (token_counts or {}).get(s)
        tok_str = f"{tok:,}" if tok else f"~{int(st['words'] * 1.3):,} (estimate)"
        rate = st["paras_ok"] / st["paras"] if st["paras"] else 0
        lines.append(f"| {s} | {st['books']:,} | {st['words']:,} | {tok_str} | {rate:.2%} |")
    tw = sum(s["words"] for s in stats.values())
    tt = sum((token_counts or {}).values()) if token_counts else None
    tt_str = f"{tt:,}" if tt else f"~{int(tw * 1.3):,} (estimate)"
    lines.append(f"| **total** | {sum(s['books'] for s in stats.values()):,} | {tw:,} | {tt_str} | {total_ok / max(total_p, 1):.2%} |")
    lines += [
        "",
        "The sanity filter is in `noirwrit/corpus/clean.py` (`paragraph_passes`): mostly letters, at least 97% ASCII, and a plausible English stopword rate.",
        "Books under 97% are dropped whole. In kept books, failing paragraphs are removed, so the training text itself is 100% passing; the column shows the rate before that step.",
    ]
    (DATA / "STATS.md").write_text("\n".join(lines) + "\n")
    (DATA / "stats.json").write_text(json.dumps({"sets": stats, "tokens": token_counts}, indent=2))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="only process the first N candidates (testing)")
    ap.add_argument("--max-general", type=int, default=600)
    a = ap.parse_args(argv)

    raw_dir = DATA / "raw"
    books = load_catalog(raw_dir / "pg_catalog.csv")
    cands = select(books, max_general=a.max_general)
    if a.limit:
        cands = cands[: a.limit]
    print(f"candidates: {len(cands)}", flush=True)

    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(process, b, raw_dir): b for b in cands}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                results.append(f.result())
            except Exception as e:  # keep going; log the failure as a drop
                results.append(Result(futs[f], "dropped", f"error: {e!r}"))
            if i % 50 == 0:
                k = sum(r.status == "kept" for r in results)
                print(f"  {i}/{len(cands)} processed, {k} pass so far", flush=True)

    ok = [r for r in results if r.status == "kept"]
    kept = dedupe(ok)
    dropped = [r for r in results if r.status == "dropped"]
    stats = write_outputs(kept, dropped)
    write_stats(stats)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
