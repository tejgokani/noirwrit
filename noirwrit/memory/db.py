"""SQLite store for everything Noirwrit remembers.

Tables from plan.md Phase 7: requests, specs, stories, chapters, summaries,
bible_entities, themes, twists, names_used. Plus chunks (retrieval), ngrams
(novelty), scenes (scene-level checkpoints) and jobs (background queue).
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY,
    created REAL NOT NULL,
    raw TEXT NOT NULL,
    spec_id INTEGER REFERENCES specs(id)
);
CREATE TABLE IF NOT EXISTS specs (
    id INTEGER PRIMARY KEY,
    created REAL NOT NULL,
    data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY,
    created REAL NOT NULL,
    spec_id INTEGER REFERENCES specs(id),
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'planned',
    outline TEXT,
    parent_story_id INTEGER REFERENCES stories(id)
);
CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    num INTEGER NOT NULL,
    title TEXT,
    text TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    words INTEGER DEFAULT 0,
    updated REAL,
    UNIQUE (story_id, num)
);
CREATE TABLE IF NOT EXISTS scenes (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    chapter_num INTEGER NOT NULL,
    num INTEGER NOT NULL,
    beat TEXT,
    text TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    tokens INTEGER DEFAULT 0,
    seconds REAL DEFAULT 0,
    UNIQUE (story_id, chapter_num, num)
);
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    chapter_num INTEGER NOT NULL,
    text TEXT NOT NULL,
    UNIQUE (story_id, chapter_num)
);
CREATE TABLE IF NOT EXISTS bible_entities (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    kind TEXT NOT NULL,
    name TEXT NOT NULL,
    data TEXT NOT NULL DEFAULT '{}',
    first_chapter INTEGER,
    UNIQUE (story_id, kind, name)
);
CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    theme TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS twists (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    twist TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS names_used (
    id INTEGER PRIMARY KEY,
    story_id INTEGER REFERENCES stories(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    role TEXT
);
CREATE INDEX IF NOT EXISTS names_used_name ON names_used(name);
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    story_id INTEGER REFERENCES stories(id) ON DELETE CASCADE,
    kind TEXT NOT NULL DEFAULT 'context',
    text TEXT NOT NULL,
    embedding BLOB NOT NULL
);
CREATE INDEX IF NOT EXISTS chunks_story ON chunks(story_id);
CREATE TABLE IF NOT EXISTS ngrams (
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    hash INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ngrams_hash ON ngrams(hash);
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    created REAL NOT NULL,
    kind TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    priority INTEGER NOT NULL DEFAULT 0,
    attempts INTEGER NOT NULL DEFAULT 0,
    worker TEXT,
    heartbeat REAL,
    error TEXT,
    progress TEXT
);
CREATE INDEX IF NOT EXISTS jobs_status ON jobs(status, priority, id);
CREATE TABLE IF NOT EXISTS live (
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    chapter_num INTEGER NOT NULL,
    scene_num INTEGER NOT NULL,
    text TEXT NOT NULL,
    updated REAL NOT NULL,
    PRIMARY KEY (story_id, chapter_num)
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


class DB:
    """Thin thread-safe wrapper. One connection per thread."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._shared = None
        if self.path == ":memory:":
            # In-memory DBs are per connection, so share one.
            self._shared = self._connect()
        self.conn.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.path, timeout=30, check_same_thread=self.path != ":memory:")
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON")
        return c

    @property
    def conn(self) -> sqlite3.Connection:
        if self._shared is not None:
            return self._shared
        c = getattr(self._local, "conn", None)
        if c is None:
            c = self._connect()
            self._local.conn = c
        return c

    def execute(self, sql: str, args: tuple | list = ()) -> sqlite3.Cursor:
        cur = self.conn.execute(sql, args)
        self.conn.commit()
        return cur

    def query(self, sql: str, args: tuple | list = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, args).fetchall()

    def one(self, sql: str, args: tuple | list = ()) -> sqlite3.Row | None:
        return self.conn.execute(sql, args).fetchone()

    # Convenience writers -------------------------------------------------

    def add_spec(self, spec: dict, raw_request: str = "") -> int:
        sid = self.execute("INSERT INTO specs(created, data) VALUES (?, ?)", (time.time(), json.dumps(spec))).lastrowid
        self.execute("INSERT INTO requests(created, raw, spec_id) VALUES (?, ?, ?)", (time.time(), raw_request or json.dumps(spec), sid))
        return int(sid)

    def specs(self) -> list[tuple[int, dict]]:
        return [(r["id"], json.loads(r["data"])) for r in self.query("SELECT id, data FROM specs ORDER BY id")]

    def requested_specs(self) -> list[tuple[int, dict]]:
        """What the user actually asked for, per spec (before the planner filled blanks)."""
        out = []
        for r in self.query("SELECT spec_id, raw FROM requests WHERE spec_id IS NOT NULL ORDER BY id"):
            try:
                raw = json.loads(r["raw"])
            except (TypeError, ValueError):
                continue
            if isinstance(raw, dict):
                out.append((r["spec_id"], {k: v for k, v in raw.items() if v not in ("", None)}))
        return out

    def get_setting(self, key: str, default=None):
        r = self.one("SELECT value FROM settings WHERE key=?", (key,))
        return json.loads(r["value"]) if r else default

    def set_setting(self, key: str, value) -> None:
        self.execute("INSERT INTO settings(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                     (key, json.dumps(value)))
