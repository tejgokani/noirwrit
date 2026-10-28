"""Download Project Gutenberg plain text politely, with retries and a gzip cache."""

from __future__ import annotations

import gzip
import time
import urllib.error
import urllib.request
from pathlib import Path

URL_TEMPLATES = (
    "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt",
    "https://www.gutenberg.org/ebooks/{id}.txt.utf-8",
)
USER_AGENT = "noirwrit-corpus/0.1 (public domain research corpus; polite, 1 req/s per worker)"


def cache_path(raw_dir: Path, book_id: int) -> Path:
    return raw_dir / "books" / f"{book_id}.txt.gz"


def fetch_book(book_id: int, raw_dir: Path, delay_s: float = 1.0, retries: int = 4) -> str | None:
    """Return the book text, from cache when present. None if every attempt fails."""
    path = cache_path(raw_dir, book_id)
    if path.exists():
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
            return f.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        for tpl in URL_TEMPLATES:
            url = tpl.format(id=book_id)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    continue
                time.sleep(delay_s * (2**attempt))
                continue
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
                time.sleep(delay_s * (2**attempt))
                continue
            text = data.decode("utf-8", errors="replace")
            tmp = path.with_suffix(".tmp")
            with gzip.open(tmp, "wt", encoding="utf-8") as f:
                f.write(text)
            tmp.replace(path)
            time.sleep(delay_s)
            return text
    return None
