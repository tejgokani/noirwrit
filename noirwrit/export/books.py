"""Offline export: TXT, Markdown, print-ready PDF, and EPUB 3 (Kindle via Send to Kindle).

PDF: title page, table of contents with page numbers, chapter openers on new
pages, page numbers, running header with the story title, serif book font.
Page sizes: A4, US Letter, A5, 6x9 in. Rendered with WeasyPrint, which embeds
(subsets) the fonts it uses.

EPUB 3: typographic cover image, nav and NCX table of contents, one XHTML file
per chapter, reflowable text, metadata (title, author "Noirwrit", language).
"""

from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path

PAGE_SIZES = {"A4": "A4", "Letter": "letter", "A5": "A5", "6x9": "6in 9in"}
AUTHOR = "Noirwrit"


@dataclass
class Book:
    title: str
    chapters: list[tuple[str, str]]  # (chapter title, text)
    author: str = AUTHOR
    language: str = "en"
    subtitle: str = ""
    identifier: str = field(default_factory=lambda: f"urn:uuid:{uuid.uuid4()}")


@dataclass
class ExportOptions:
    page_size: str = "6x9"
    font_size_pt: float = 11.0
    include_cover: bool = True
    include_toc: bool = True


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


# Plain text and Markdown --------------------------------------------------

def to_txt(book: Book) -> str:
    out = [book.title.upper(), f"by {book.author}", ""]
    for i, (title, text) in enumerate(book.chapters, 1):
        out += ["", f"CHAPTER {i}. {title.upper()}", ""]
        out += [p + "\n" for p in paragraphs(text)]
    return "\n".join(out).rstrip() + "\n"


def to_md(book: Book) -> str:
    out = [f"# {book.title}", "", f"*by {book.author}*", ""]
    for i, (title, text) in enumerate(book.chapters, 1):
        out += [f"## Chapter {i}: {title}", ""]
        out += [p + "\n" for p in paragraphs(text)]
    return "\n".join(out).rstrip() + "\n"


# HTML for print -----------------------------------------------------------

def _esc(s: str) -> str:
    return html.escape(s, quote=False)


def print_css(opts: ExportOptions, title: str) -> str:
    size = PAGE_SIZES.get(opts.page_size, "6in 9in")
    small = opts.page_size in ("A5", "6x9")
    margin = "18mm 16mm 20mm 18mm" if small else "24mm 22mm 26mm 24mm"
    t = title.replace('"', "'")
    return f"""
@page {{
  size: {size};
  margin: {margin};
  @top-center {{ content: string(booktitle); font-family: "Baskerville", "Georgia", "Times New Roman", serif;
                 font-size: 8.5pt; font-style: italic; color: #555; }}
  @bottom-center {{ content: counter(page); font-family: "Baskerville", "Georgia", serif; font-size: 9pt; }}
}}
@page :first {{ @top-center {{ content: none; }} @bottom-center {{ content: none; }} }}
@page front {{ @top-center {{ content: none; }} @bottom-center {{ content: none; }} }}
@page chapter {{ }}
@page chapter:nth(1 of chapter) {{ @top-center {{ content: none; }} }}
html {{ string-set: booktitle "{t}"; }}
body {{ font-family: "Baskerville", "Palatino", "Georgia", "Times New Roman", serif;
        font-size: {opts.font_size_pt}pt; line-height: 1.42; color: #111; hyphens: auto; }}
.cover, .titlepage, .toc {{ page: front; page-break-after: always; text-align: center; }}
.cover {{ height: 100%; display: flex; flex-direction: column; justify-content: center; }}
.cover h1 {{ font-size: 30pt; letter-spacing: 0.06em; text-transform: uppercase; margin: 0 0 8mm; }}
.cover .rule {{ width: 30%; margin: 0 auto 8mm; border-top: 1.5pt solid #111; }}
.cover .by {{ font-size: 12pt; letter-spacing: 0.25em; text-transform: uppercase; }}
.titlepage h1 {{ font-size: 22pt; margin-top: 35%; font-weight: normal; }}
.titlepage .by {{ font-style: italic; margin-top: 6mm; }}
.toc {{ text-align: left; }}
.toc h2 {{ text-align: center; font-weight: normal; letter-spacing: 0.2em; text-transform: uppercase; font-size: 12pt; margin-bottom: 8mm; }}
.toc ol {{ list-style: none; padding: 0; }}
.toc li {{ margin: 2.5mm 0; }}
.toc a {{ color: inherit; text-decoration: none; }}
.toc a::after {{ content: leader(".") target-counter(attr(href), page); }}
section.chapter {{ page: chapter; page-break-before: always; }}
section.chapter h2 {{ font-weight: normal; text-align: center; margin: 18% 0 10mm; font-size: 15pt; }}
section.chapter h2 .num {{ display: block; font-size: 9.5pt; letter-spacing: 0.3em; text-transform: uppercase; margin-bottom: 3mm; }}
p {{ margin: 0; text-indent: 1.4em; text-align: justify; orphans: 2; widows: 2; }}
h2 + p {{ text-indent: 0; }}
"""


def to_html(book: Book, opts: ExportOptions | None = None) -> str:
    opts = opts or ExportOptions()
    parts = [f"<!doctype html><html lang='{book.language}'><head><meta charset='utf-8'>"
             f"<title>{_esc(book.title)}</title><style>{print_css(opts, book.title)}</style></head><body>"]
    if opts.include_cover:
        parts.append(f"<div class='cover'><h1>{_esc(book.title)}</h1><div class='rule'></div>"
                     f"<div class='by'>{_esc(book.author)}</div></div>")
    parts.append(f"<div class='titlepage'><h1>{_esc(book.title)}</h1><div class='by'>by {_esc(book.author)}</div></div>")
    if opts.include_toc and len(book.chapters) > 1:
        items = "".join(f"<li><a href='#ch{i}'>{i}. {_esc(t)}</a></li>" for i, (t, _) in enumerate(book.chapters, 1))
        parts.append(f"<div class='toc'><h2>Contents</h2><ol>{items}</ol></div>")
    for i, (title, text) in enumerate(book.chapters, 1):
        body = "".join(f"<p>{_esc(p)}</p>" for p in paragraphs(text))
        parts.append(f"<section class='chapter' id='ch{i}'><h2><span class='num'>Chapter {i}</span>{_esc(title)}</h2>{body}</section>")
    parts.append("</body></html>")
    return "".join(parts)


# PDF ----------------------------------------------------------------------

def _weasy_env() -> dict:
    env = dict(os.environ)
    if sys.platform == "darwin":
        extra = [p for p in ("/opt/homebrew/lib", "/usr/local/lib") if Path(p).exists()]
        env["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(extra + [env.get("DYLD_FALLBACK_LIBRARY_PATH", "")]).strip(":")
    return env


_weasy_inproc: bool | None = None


def _can_import_weasy() -> bool:
    """Try the in-process import once, quietly (WeasyPrint prints a banner when its libs are missing)."""
    global _weasy_inproc
    if _weasy_inproc is None:
        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                import weasyprint  # noqa: F401

                _weasy_inproc = True
            except OSError:
                _weasy_inproc = False
    return _weasy_inproc


def render_pdf(html_text: str, out: Path) -> Path:
    """Render HTML to PDF with WeasyPrint, in-process when its native libs load, else in a subprocess."""
    out.parent.mkdir(parents=True, exist_ok=True)
    if not _can_import_weasy():
        src = out.with_suffix(".src.html")
        src.write_text(html_text)
        code = ("import sys, weasyprint; "
                "weasyprint.HTML(filename=sys.argv[1]).write_pdf(sys.argv[2])")
        try:
            subprocess.run([sys.executable, "-c", code, str(src), str(out)], check=True, env=_weasy_env(),
                           capture_output=True, timeout=600)
        finally:
            src.unlink(missing_ok=True)
        return out
    import weasyprint

    weasyprint.HTML(string=html_text).write_pdf(str(out))
    return out


def to_pdf(book: Book, out: Path, opts: ExportOptions | None = None) -> Path:
    return render_pdf(to_html(book, opts), out)


def open_print_dialog(pdf: Path) -> None:
    """Open the PDF in the system viewer (Preview on macOS), where Cmd+P prints it."""
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(pdf)])
    elif shutil.which("xdg-open"):
        subprocess.Popen(["xdg-open", str(pdf)])


# EPUB ---------------------------------------------------------------------

def cover_png(title: str, author: str = AUTHOR, size=(1600, 2560)) -> bytes:
    """Plain typographic cover: black field, cream title, thin rule. No AI images."""
    import io

    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", size, (14, 14, 14))
    d = ImageDraw.Draw(img)
    fonts = ["/System/Library/Fonts/Supplemental/Baskerville.ttc", "/System/Library/Fonts/Supplemental/Georgia.ttf",
             "/Library/Fonts/Georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
    path = next((f for f in fonts if Path(f).exists()), None)

    def font(px: int):
        return ImageFont.truetype(path, px) if path else ImageFont.load_default()

    cream, accent = (236, 228, 210), (122, 214, 196)
    words, lines, cur = title.upper().split(), [], ""
    f = font(150)
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) > size[0] * 0.8 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    y = size[1] * 0.32
    for ln in lines:
        wpx = d.textlength(ln, font=f)
        d.text(((size[0] - wpx) / 2, y), ln, font=f, fill=cream)
        y += 185
    y += 60
    d.line([(size[0] * 0.38, y), (size[0] * 0.62, y)], fill=accent, width=6)
    fa = font(70)
    a = author.upper()
    d.text(((size[0] - d.textlength(a, font=fa)) / 2, y + 80), a, font=fa, fill=cream)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


EPUB_CSS = """
body { font-family: serif; line-height: 1.45; margin: 0 4%; }
h1 { text-align: center; font-weight: normal; margin-top: 30%; }
h2 { text-align: center; font-weight: normal; margin: 2em 0 1.2em; }
h2 .num { display: block; font-size: 0.7em; letter-spacing: 0.3em; text-transform: uppercase; }
p { margin: 0; text-indent: 1.4em; text-align: justify; }
h2 + p { text-indent: 0; }
"""


def to_epub(book: Book, out: Path, opts: ExportOptions | None = None) -> Path:
    from ebooklib import epub

    opts = opts or ExportOptions()
    eb = epub.EpubBook()
    eb.set_identifier(book.identifier)
    eb.set_title(book.title)
    eb.set_language(book.language)
    eb.add_author(book.author)
    eb.add_metadata("DC", "publisher", "Noirwrit")
    if opts.include_cover:
        eb.set_cover("cover.png", cover_png(book.title, book.author))
    css = epub.EpubItem(uid="style", file_name="style/book.css", media_type="text/css", content=EPUB_CSS)
    eb.add_item(css)

    title_page = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang=book.language)
    title_page.content = f"<h1>{_esc(book.title)}</h1><p style='text-align:center;text-indent:0'><em>by {_esc(book.author)}</em></p>"
    title_page.add_item(css)
    eb.add_item(title_page)

    chapters = []
    for i, (title, text) in enumerate(book.chapters, 1):
        c = epub.EpubHtml(title=f"{i}. {title}", file_name=f"chapter_{i:03d}.xhtml", lang=book.language)
        body = "".join(f"<p>{_esc(p)}</p>" for p in paragraphs(text))
        c.content = f"<h2><span class='num'>Chapter {i}</span>{_esc(title)}</h2>{body}"
        c.add_item(css)
        eb.add_item(c)
        chapters.append(c)

    eb.toc = tuple(chapters)
    eb.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    eb.add_item(nav)
    spine: list = ["cover"] if opts.include_cover else []
    spine += [title_page]
    if opts.include_toc:
        spine.append("nav")
    eb.spine = spine + chapters
    out.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(out), eb)
    return out


def epubcheck(path: Path) -> tuple[bool, str] | None:
    """Validate with epubcheck if available (CLI or jar in ~/.noirwrit/tools). None if not installed."""
    from noirwrit.config import HOME

    exe = shutil.which("epubcheck")
    jar = next(iter(sorted((HOME / "tools").glob("epubcheck*/epubcheck.jar"))), None) if (HOME / "tools").exists() else None
    if exe:
        cmd = [exe, str(path)]
    elif jar and shutil.which("java"):
        cmd = ["java", "-jar", str(jar), str(path)]
    else:
        return None
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, (r.stdout + r.stderr)[-4000:]


KINDLE_STEPS = [
    "USB or the Send to Kindle app: drag the EPUB into the Send to Kindle desktop app, or copy it to the Kindle's documents folder over USB.",
    "Web: open amazon.com/sendtokindle, sign in, and drop the EPUB onto the page.",
    "Email: attach the EPUB to an email sent to your Kindle address (Manage Your Content and Devices, Preferences, Personal Document Settings). Add your sending address to the approved list first.",
]


def save_for_kindle(book: Book, folder: Path, opts: ExportOptions | None = None) -> dict:
    """Write the EPUB where the user wants it and return the three transfer options. Never sends anything."""
    safe = re.sub(r"[^A-Za-z0-9 _-]+", "", book.title).strip().replace(" ", "_") or "noirwrit_book"
    path = to_epub(book, folder / f"{safe}.epub", opts)
    res = {"path": str(path), "steps": KINDLE_STEPS}
    if shutil.which("ebook-convert"):
        res["calibre"] = "Calibre found: older Kindles can use AZW3 via 'Convert to AZW3'."
    return res


def to_azw3(epub_path: Path) -> Path:
    """Optional, for older Kindles. Requires Calibre's ebook-convert."""
    exe = shutil.which("ebook-convert")
    if not exe:
        raise RuntimeError("Calibre is not installed")
    out = epub_path.with_suffix(".azw3")
    subprocess.run([exe, str(epub_path), str(out)], check=True, capture_output=True, timeout=600)
    return out
