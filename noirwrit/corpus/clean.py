"""Clean Project Gutenberg plain text into training prose.

Steps: strip the PG header and footer, fix encoding leftovers, normalize quotes
and whitespace, drop tables of contents, illustration tags, and other
front/back matter junk.
"""

from __future__ import annotations

import re
import unicodedata

START_RE = re.compile(r"^\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\s*$", re.I | re.M)
END_RE = re.compile(r"^\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\s*$", re.I | re.M)
# Older files use different markers.
OLD_START_RE = re.compile(r"^\*END\*THE SMALL PRINT!.*$", re.I | re.M)
OLD_END_RE = re.compile(r"^(End of (the )?Project Gutenberg'?s? .*|End of this Project Gutenberg.*)$", re.I | re.M)

COPYRIGHT_YEAR_RE = re.compile(
    r"(?:copyright(?:ed)?|\(c\)|©)[,.\s]*(?:in\s+)?(?:the\s+year\s+)?(1[89]\d\d)", re.I
)
PUBLISHED_YEAR_RE = re.compile(
    r"(?:published|first (?:printing|edition)|printed|produced from|transcribed from|"
    r"originally appeared in|appeared in)[^\n]{0,80}?(1[89]\d\d)",
    re.I,
)

JUNK_LINE_RE = re.compile(
    r"^\s*(\[(illustration|frontispiece|transcriber'?s? note|footnote|sidenote|pg)[^\]]*\]?|"
    r"produced by .*|transcribed from .*|e-?text prepared by .*|"
    r"(this )?e-?book (was )?(produced|prepared) by .*)\s*$",
    re.I,
)
CHAPTER_HEAD_RE = re.compile(
    r"^\s*(chapter|book|part|story|section)\s+([ivxlcdm]+|\d+|[a-z-]+)\b.{0,80}$", re.I
)
TOC_HEAD_RE = re.compile(r"^\s*(contents|table of contents|list of illustrations|illustrations)\s*\.?\s*$", re.I)

QUOTE_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "«": '"', "»": '"',
    "′": "'", "″": '"',
    # Em and en dashes become plain separators; the project style avoids em dashes.
    "—": " - ", "–": "-", "‒": "-", "―": " - ",
    "…": "...",
    " ": " ", " ": " ", " ": " ", " ": " ",
    "﻿": "", "​": "", "­": "",
}
QUOTE_TABLE = str.maketrans(QUOTE_MAP)

# Common mojibake from UTF-8 read as cp1252.
MOJIBAKE = {
    "â€œ": '"', "â€\x9d": '"', "â€™": "'", "â€˜": "'", "â€”": " - ", "â€“": "-",
    "â€¦": "...", "Ã©": "é", "Ã¨": "è", "Ã ": "à", "Ã¢": "â", "Ã§": "ç",
}


def strip_gutenberg(text: str) -> tuple[str, str]:
    """Return (header, body). The header is kept so we can read copyright lines."""
    m = START_RE.search(text) or OLD_START_RE.search(text)
    if m:
        header, body = text[: m.end()], text[m.end():]
    else:
        header, body = "", text
    e = END_RE.search(body) or OLD_END_RE.search(body)
    if e:
        body = body[: e.start()]
    return header, body


def front_matter_years(body: str, header: str = "", lines: int = 250) -> list[int]:
    """Years from copyright or 'published' statements near the start of the book."""
    head = header[-3000:] + "\n" + "\n".join(body.splitlines()[:lines])
    years = [int(y) for y in COPYRIGHT_YEAR_RE.findall(head)]
    years += [int(y) for y in PUBLISHED_YEAR_RE.findall(head)]
    return sorted(set(years))


def header_says_copyrighted(header: str) -> bool:
    """PG marks the few copyrighted texts it hosts in the header."""
    h = header.lower()
    return "copyrighted project gutenberg" in h or "this is a copyrighted" in h


def fix_encoding(text: str) -> str:
    for bad, good in MOJIBAKE.items():
        text = text.replace(bad, good)
    text = unicodedata.normalize("NFC", text)
    return text.translate(QUOTE_TABLE)


def _is_prose_run(lines: list[str], j: int) -> bool:
    """True if a hard-wrapped prose paragraph starts at j: 3+ consecutive long lines."""
    run = lines[j:j + 3]
    return len(run) == 3 and all(len(s.strip()) > 45 for s in run)


def _drop_toc(lines: list[str]) -> list[str]:
    """Remove a CONTENTS block: the heading plus the entries up to the first prose paragraph.

    Entries are usually short lines, separated by blanks or single. Prose in PG
    files is hard-wrapped near 70 columns, so the block ends at the first run of
    long consecutive lines. It also ends at the second chapter heading that
    repeats the first entry, since many books restate "CHAPTER I" in the body.
    """
    out: list[str] = []
    i = 0
    while i < len(lines):
        if TOC_HEAD_RE.match(lines[i]):
            j = i + 1
            entries: list[str] = []
            while j < len(lines) and j - i < 300:
                s = lines[j].strip()
                if s and _is_prose_run(lines, j):
                    break
                if s:
                    if entries and s.lower() == entries[0].lower():
                        break  # body starts with the first TOC entry repeated
                    entries.append(s)
                j += 1
            if len(entries) >= 3:
                # Keep the heading that starts the body, if the loop stopped on one.
                back = j
                while back > i + 1 and lines[back - 1].strip() and not _is_prose_run(lines, back - 1):
                    if CHAPTER_HEAD_RE.match(lines[back - 1]) or lines[back - 1].strip().isupper():
                        back -= 1
                    else:
                        break
                i = back
                continue
        out.append(lines[i])
        i += 1
    return out


def clean_text(body: str) -> str:
    text = fix_encoding(body)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Underscore italics and bracket notes.
    text = re.sub(r"_([^_\n]{1,200})_", r"\1", text)
    text = re.sub(r"\[(Illustration|Footnote|Sidenote)[^\]]*\]", "", text, flags=re.I | re.S)
    lines = [ln.rstrip() for ln in text.split("\n")]
    lines = [ln for ln in lines if not JUNK_LINE_RE.match(ln)]
    lines = _drop_toc(lines)

    # Rejoin hard-wrapped paragraphs. Blank lines separate paragraphs.
    paras: list[str] = []
    cur: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(s)
    if cur:
        paras.append(" ".join(cur))

    kept = []
    for p in paras:
        p = re.sub(r"[ \t]+", " ", p).strip()
        if not p:
            continue
        # Lines of only symbols, page numbers, or separators.
        if re.fullmatch(r"[\W\d_]+", p):
            continue
        if re.fullmatch(r"(page\s*)?\d+", p, re.I):
            continue
        # Mark chapter headings so the model learns structure.
        if CHAPTER_HEAD_RE.match(p) and len(p) < 90:
            kept.append("\n" + p.upper() if p.isupper() else "\n" + p)
            continue
        kept.append(p)
    out = "\n\n".join(kept)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip() + "\n"


STOPWORDS = frozenset(
    "the and of to a in that it was he i his you with as for had is her not but at on she be "
    "they have him said by from my all were this which so there one we no would me an or what "
    "if when been them their are out up could into did then".split()
)


def english_ratio(text: str) -> float:
    """Share of words that are common English stopwords. English prose sits near 0.4-0.5."""
    words = re.findall(r"[A-Za-z']+", text.lower())
    if not words:
        return 0.0
    return sum(w in STOPWORDS for w in words) / len(words)


def paragraph_passes(p: str) -> bool:
    """Basic language sanity check used for the 99% acceptance gate."""
    if len(p) < 20:
        return True  # short dialogue lines and headings are fine
    letters = sum(c.isalpha() for c in p)
    if letters / max(len(p), 1) < 0.6:
        return False
    ascii_share = sum(ord(c) < 128 for c in p) / len(p)
    if ascii_share < 0.97:
        return False
    return english_ratio(p) >= 0.15 if len(p) > 120 else True
