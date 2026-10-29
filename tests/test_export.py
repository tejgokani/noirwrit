import zipfile

import pytest

from noirwrit.export import books as ex

BOOK = ex.Book("The Crimson Ledger", [(f"Chapter {i}", "The rain kept on.\n\n\"Where?\" she asked.") for i in range(1, 4)])


@pytest.mark.parametrize("cover", [True, False])
def test_epub_structure(tmp_path, cover):
    p = ex.to_epub(BOOK, tmp_path / "b.epub", ex.ExportOptions(include_cover=cover))
    with zipfile.ZipFile(p) as z:
        names = z.namelist()
        assert names[0] == "mimetype" and z.read("mimetype") == b"application/epub+zip"
        assert sum("chapter_" in n for n in names) == 3
        opf = z.read("EPUB/content.opf").decode()
        assert "<dc:creator" in opf and "Noirwrit" in opf and "<dc:language>en</dc:language>" in opf
        assert 'linear="no"' not in opf  # epubcheck OPF-096
        assert ("cover.png" in names[0] + " ".join(names)) == cover


@pytest.mark.parametrize("cover", [True, False])
def test_epub_passes_epubcheck(tmp_path, cover):
    p = ex.to_epub(BOOK, tmp_path / "b.epub", ex.ExportOptions(include_cover=cover))
    res = ex.epubcheck(p)
    if res is None:
        pytest.skip("epubcheck not installed")
    ok, log = res
    assert ok, log


def test_txt_and_md():
    assert ex.to_txt(BOOK).startswith("THE CRIMSON LEDGER\nby Noirwrit")
    md = ex.to_md(BOOK)
    assert md.startswith("# The Crimson Ledger") and md.count("## Chapter") == 3
