from noirwrit.corpus.build import Result, dedupe
from noirwrit.corpus.catalog import Book, classify, parse_people, pd_by_metadata
from noirwrit.corpus.clean import (
    clean_text,
    front_matter_years,
    paragraph_passes,
    strip_gutenberg,
)

PG = """The Project Gutenberg eBook of Test

*** START OF THE PROJECT GUTENBERG EBOOK TEST ***

Produced by Someone

CONTENTS

STORY OF THE DOOR
SEARCH FOR MR. HYDE
DR. JEKYLL WAS QUITE AT EASE

STORY OF THE DOOR

Mr. Utterson the lawyer was a man of a rugged countenance that was never
lighted by a smile; cold, scanty and embarrassed in discourse; backward
in sentiment; lean, long, dusty, dreary and yet somehow lovable.

[Illustration: a door]

“It’s a fine night,” said he—quietly.

*** END OF THE PROJECT GUTENBERG EBOOK TEST ***
license junk here
"""


def test_strip_and_clean_keeps_first_chapter():
    header, body = strip_gutenberg(PG)
    assert "START OF" in header
    assert "license junk" not in body
    text = clean_text(body)
    assert "Mr. Utterson the lawyer was a man of a rugged countenance" in text
    assert "SEARCH FOR MR. HYDE" not in text  # TOC entry removed
    assert "STORY OF THE DOOR" in text  # chapter heading kept
    assert "Illustration" not in text
    assert "Produced by" not in text
    assert "—" not in text and "“" not in text
    assert '"It\'s a fine night," said he - quietly.' in text


def test_hard_wrapped_paragraph_rejoined():
    text = clean_text("one two three\nfour five six\n\nnext para\n")
    assert text == "one two three four five six\n\nnext para\n"


def test_front_matter_years():
    body = "THE BOOK\n\nCopyright, 1922, by Somebody\n\nPrinted in 1923\n" + "x\n" * 10
    assert front_matter_years(body) == [1922, 1923]


def test_paragraph_sanity():
    assert paragraph_passes("He said that it was a cold night and the fog had come in off the river again.")
    assert not paragraph_passes("1234 5678 ---- |||| 9999 0000 ==== 1111 2222 3333 #### $$$$ %%%% ^^^^")


def _book(title, authors, subjects="Detective and mystery stories"):
    return Book(1, title, parse_people(authors), subjects, "", "PR")


def test_pd_rules():
    ok, why = pd_by_metadata(_book("A Study in Scarlet", "Doyle, Arthur Conan, 1859-1930"))
    assert ok is True and "1930" in why
    ok, _ = pd_by_metadata(_book("The Maltese falcon", "Hammett, Dashiell, 1894-1961"))
    assert ok is True
    ok, _ = pd_by_metadata(_book("Some later novel", "Hammett, Dashiell, 1894-1961"))
    assert ok is None  # needs dated front matter
    ok, _ = pd_by_metadata(_book("Nick Carter Stories No. 131, March 13, 1915: A fatal message", "Carter, Nicholas (House name)"))
    assert ok is True
    ok, _ = pd_by_metadata(_book("Space story", "Writer, Young, 1925-1990"))
    assert ok is False


def test_classify_sets():
    assert classify(_book("The Maltese falcon", "Hammett, Dashiell, 1894-1961")) == "noir"
    assert classify(_book("A Study in Scarlet", "Doyle, Arthur Conan, 1859-1930")) == "crime"
    assert classify(_book("Collected poems of Someone", "Doyle, Arthur Conan, 1859-1930")) == ""


def _word(i: int, prefix: str) -> str:
    # Letters only, since the shingler ignores digits.
    s = ""
    while True:
        s = chr(97 + i % 26) + s
        i //= 26
        if not i:
            return prefix + s


def test_dedupe_drops_contained_story():
    words = [_word(i, "w") for i in range(6000)]
    big = " ".join(words)
    small = " ".join(words[1000:3000])
    other = " ".join(_word(i, "z") for i in range(3000))
    rs = [
        Result(_book("Collection", "A, B, 1800-1850"), "kept", text=big, words=6000),
        Result(_book("Story", "A, B, 1800-1850"), "kept", text=small, words=2000),
        Result(_book("Other", "A, B, 1800-1850"), "kept", text=other, words=3000),
    ]
    kept = dedupe(rs)
    titles = sorted(r.book.title for r in kept)
    assert titles == ["Collection", "Other"]
