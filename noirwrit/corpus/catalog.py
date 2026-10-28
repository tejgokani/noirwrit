"""Select public domain books from the Project Gutenberg catalog CSV.

Public domain rule (US, as of 2026): published in 1930 or earlier.
A book qualifies when one of these holds:
  1. Every listed contributor (author, translator, editor) died in 1930 or
     earlier, so nothing they wrote can be newer than 1930.
  2. The title is in KNOWN_YEARS with a first publication year of 1930 or earlier.
  3. The book's own front matter (checked after download) carries a
     copyright or publication year, and the latest such year is 1930 or earlier.
Anything else is left out. Rule 3 runs in build.py because it needs the text.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

PD_CUTOFF = 1930

PERSON_RE = re.compile(
    r"^(?P<name>[^\[]+?)(?:,\s*(?P<born>\d{3,4})?\??(?:\s*BCE)?-(?P<died>\d{3,4})?\??)?\s*(?:\[(?P<role>[^\]]+)\])?$"
)

# Well established first publication years for authors who lived past 1930.
# Key: (surname, lowercase title fragment). Value: (year, note).
KNOWN_YEARS: dict[tuple[str, str], tuple[int, str]] = {
    ("christie", "mysterious affair at styles"): (1920, "first published 1920"),
    ("christie", "secret adversary"): (1922, "first published 1922"),
    ("christie", "murder on the links"): (1923, "first published 1923"),
    ("christie", "poirot investigates"): (1924, "collection, first published 1924"),
    ("christie", "man in the brown suit"): (1924, "first published 1924"),
    ("christie", "secret of chimneys"): (1925, "first published 1925"),
    ("christie", "murder of roger ackroyd"): (1926, "first published 1926"),
    ("christie", "big four"): (1927, "first published 1927"),
    ("christie", "mystery of the blue train"): (1928, "first published 1928"),
    ("christie", "seven dials mystery"): (1929, "first published 1929"),
    ("christie", "partners in crime"): (1929, "collection, first published 1929"),
    ("christie", "murder at the vicarage"): (1930, "first published 1930"),
    ("christie", "mysterious mr. quin"): (1930, "collection, first published 1930"),
    ("hammett", "red harvest"): (1929, "first published in book form 1929"),
    ("hammett", "dain curse"): (1929, "first published in book form 1929"),
    ("hammett", "maltese falcon"): (1930, "first published in book form 1930"),
    ("chesterton", "innocence of father brown"): (1911, "first published 1911"),
    ("chesterton", "wisdom of father brown"): (1914, "first published 1914"),
    ("chesterton", "incredulity of father brown"): (1926, "first published 1926"),
    ("chesterton", "secret of father brown"): (1927, "first published 1927"),
    ("chesterton", "man who was thursday"): (1908, "first published 1908"),
    ("chesterton", "club of queer trades"): (1905, "first published 1905"),
    ("chesterton", "man who knew too much"): (1922, "first published 1922"),
    ("burnett", "little caesar"): (1929, "first published 1929"),
    ("green", "leavenworth case"): (1878, "first published 1878"),
    ("rinehart", "circular staircase"): (1908, "first published 1908"),
    ("rinehart", "man in lower ten"): (1909, "first published 1909"),
    ("rinehart", "window at the white cat"): (1910, "first published 1910"),
    ("wallace", "four just men"): (1905, "first published 1905"),
    ("freeman", "red thumb mark"): (1907, "first published 1907"),
    ("leblanc", "gentleman burglar"): (1910, "English translation 1910"),
    ("leblanc", "arsène lupin versus herlock sholmes"): (1910, "English translation 1910"),
    ("leblanc", "hollow needle"): (1910, "English translation 1910"),
    ("biggers", "house without a key"): (1925, "first published 1925"),
    ("biggers", "seven keys to baldpate"): (1913, "first published 1913"),
    ("sayers", "whose body"): (1923, "first published 1923"),
    ("sayers", "clouds of witness"): (1926, "first published 1926"),
    ("sayers", "unnatural death"): (1927, "first published 1927"),
    ("van dine", "benson murder case"): (1926, "first published 1926"),
    ("van dine", "canary\" murder case"): (1927, "first published 1927"),
    ("van dine", "greene murder case"): (1928, "first published 1928"),
    ("van dine", "bishop murder case"): (1929, "first published 1929"),
    ("sayers", "unpleasantness at the bellona club"): (1928, "first published 1928"),
    ("sayers", "lord peter views the body"): (1928, "collection, first published 1928"),
    ("charteris", "meet the tiger"): (1928, "first published 1928"),
    ("allingham", "crime at black dudley"): (1929, "first published 1929"),
    ("morrison", "martin hewitt, investigator"): (1894, "collection, first published 1894"),
    ("morrison", "chronicles of martin hewitt"): (1895, "collection, first published 1895"),
    ("morrison", "adventures of martin hewitt"): (1896, "collection, first published 1896"),
    ("morrison", "red triangle"): (1903, "collection, first published 1903"),
    ("morrison", "dorrington deed-box"): (1897, "collection, first published 1897"),
    ("bramah", "max carrados"): (1914, "collection, first published 1914"),
    ("shiel", "prince zaleski"): (1895, "collection, first published 1895"),
    ("packard", "adventures of jimmie dale"): (1917, "first published 1917"),
    ("packard", "further adventures of jimmie dale"): (1919, "first published 1919"),
    ("packard", "white moll"): (1920, "first published 1920"),
    ("packard", "miracle man"): (1914, "first published 1914"),
    ("packard", "doors of the night"): (1922, "first published 1922"),
    ("packard", "night operator"): (1919, "first published 1919"),
    ("packard", "wire devils"): (1918, "first published 1918"),
    ("packard", "from now on"): (1919, "first published 1919"),
    ("packard", "pawned"): (1921, "first published 1921"),
    ("packard", "sin that was his"): (1917, "first published 1917"),
    ("packard", "four stragglers"): (1923, "first published 1923"),
}

# Authors and series that make up the noir voice set: American hardboiled and
# pulp crime. Every pick still needs one of the PD rules above.
NOIR_AUTHORS = (
    "hammett", "burnett, w. r.", "daly, carroll john", "whitfield, raoul", "nebel, frederick",
    "packard, frank", "carter, nicholas",
)
NOIR_EXCLUDE_TITLE_RE = re.compile(r"beloved traitor|belovéd traitor|on the iron at big cloud", re.I)

# A full date in the title, as in pulp weeklies: "No. 131, March 13, 1915".
TITLE_DATE_RE = re.compile(
    r"(?:january|february|march|april|may|june|july|august|september|october|november|december)"
    r"\s+\d{1,2},?\s+(1[89]\d\d)",
    re.I,
)

CRIME_SUBJECT_RE = re.compile(
    r"detective and mystery|mystery fiction|crime\b.*fiction|murder\b.*fiction|criminals\b.*fiction|"
    r"private investigators|police\b.*fiction|thieves\b.*fiction|swindlers|holmes, sherlock|"
    r"brown, father|poirot|lupin|detectives\b",
    re.I,
)
CRIME_SHELF_RE = re.compile(r"detective fiction|crime, thrillers and mystery|crime fiction|mystery fiction", re.I)
GENERAL_SUBJECT_RE = re.compile(
    r"adventure stories|gothic fiction|horror tales|sea stories|ghost stories|suspense fiction|"
    r"spy stories|historical fiction|western stories",
    re.I,
)
GENERAL_SHELF_RE = re.compile(r"adventure|gothic fiction|horror|ghost stor", re.I)
FICTION_LOCC_RE = re.compile(r"\bP[RSZQ]\b|^P[RSZQ]")
EXCLUDE_TITLE_RE = re.compile(
    r"\b(index|bibliography|catalog(ue)?|dictionary|magazine,? vol|volume \d+ of the complete|"
    r"complete works|works of|collected works|letters of|plays?\b|poems?\b|audio)\b",
    re.I,
)


@dataclass
class Person:
    name: str
    born: int | None
    died: int | None
    role: str | None

    @property
    def surname(self) -> str:
        return self.name.split(",")[0].strip().lower()


@dataclass
class Book:
    id: int
    title: str
    authors: list[Person]
    subjects: str
    bookshelves: str
    locc: str
    set: str = ""
    pd_basis: str = ""
    year: int | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def author_line(self) -> str:
        names = [p.name for p in self.authors if not p.role or p.role.lower() in ("author", "contributor")]
        return "; ".join(names) or "Anonymous"

    @property
    def primary_surname(self) -> str:
        for p in self.authors:
            if not p.role or p.role.lower() == "author":
                return p.surname
        return self.authors[0].surname if self.authors else ""


def parse_people(field_: str) -> list[Person]:
    out = []
    for raw in field_.split(";"):
        raw = raw.strip()
        if not raw:
            continue
        m = PERSON_RE.match(raw)
        if not m:
            out.append(Person(raw, None, None, None))
            continue
        born = int(m.group("born")) if m.group("born") else None
        died = int(m.group("died")) if m.group("died") else None
        out.append(Person(m.group("name").strip().rstrip(","), born, died, m.group("role")))
    return out


def load_catalog(path: Path) -> list[Book]:
    books = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("Type") != "Text" or row.get("Language") != "en":
                continue
            try:
                bid = int(row["Text#"])
            except (KeyError, ValueError):
                continue
            books.append(Book(
                id=bid,
                title=" ".join(row.get("Title", "").split()),
                authors=parse_people(row.get("Authors", "")),
                subjects=row.get("Subjects", ""),
                bookshelves=row.get("Bookshelves", ""),
                locc=row.get("LoCC", ""),
            ))
    return books


def known_year(book: Book) -> tuple[int, str] | None:
    title = book.title.lower()
    for (surname, frag), val in KNOWN_YEARS.items():
        if frag in title and any(surname in p.name.lower() for p in book.authors):
            return val
    return None


def pd_by_metadata(book: Book) -> tuple[bool | None, str]:
    """True if PD is proven from metadata, False if ruled out, None if the text must decide."""
    kn = known_year(book)
    if kn:
        year, note = kn
        if year <= PD_CUTOFF:
            book.year = year
            return True, f"known first publication: {note}"
        return False, f"known first publication {year}, after {PD_CUTOFF}"
    td = TITLE_DATE_RE.search(book.title)
    if td:
        year = int(td.group(1))
        if year <= PD_CUTOFF:
            book.year = year
            return True, f"issue dated {year} in the title"
        return False, f"issue dated {year}, after {PD_CUTOFF}"
    if not book.authors:
        return None, "no contributors listed"
    if any(p.born and p.born > PD_CUTOFF - 15 for p in book.authors):
        return False, "a contributor was born too late to publish by 1930"
    if all(p.died is not None and p.died <= PD_CUTOFF for p in book.authors):
        died = max(p.died for p in book.authors)  # type: ignore[type-var]
        return True, f"all contributors died by {died}"
    return None, "contributor alive after 1930; needs a dated front matter"


def classify(book: Book) -> str:
    """Return 'noir', 'crime', 'general', or '' (skip)."""
    if EXCLUDE_TITLE_RE.search(book.title):
        return ""
    names = " ".join(p.name.lower() for p in book.authors)
    if any(a in names for a in NOIR_AUTHORS) and not NOIR_EXCLUDE_TITLE_RE.search(book.title):
        return "noir"
    if CRIME_SUBJECT_RE.search(book.subjects) or CRIME_SHELF_RE.search(book.bookshelves):
        return "crime"
    is_fiction = "fiction" in book.subjects.lower() or bool(FICTION_LOCC_RE.search(book.locc))
    if is_fiction and (GENERAL_SUBJECT_RE.search(book.subjects) or GENERAL_SHELF_RE.search(book.bookshelves)):
        return "general"
    return ""


def select(books: list[Book], max_general: int = 600) -> list[Book]:
    """Candidates per set. PD may still be undecided (None) for some; build.py settles it."""
    picked: list[Book] = []
    general = 0
    for b in sorted(books, key=lambda x: x.id):
        s = classify(b)
        if not s:
            continue
        ok, why = pd_by_metadata(b)
        if ok is False:
            continue
        if s == "general":
            if general >= max_general:
                continue
            general += 1
        b.set = s
        b.pd_basis = why if ok else ""
        if ok is None:
            b.notes.append(why)
        picked.append(b)
    return picked
