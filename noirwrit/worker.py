"""Background generation worker with a SQLite job queue.

- Jobs survive restarts: a job whose heartbeat goes stale is requeued.
- Scene-level checkpoints come from the story engine; a resumed job skips done scenes.
- Prefetch: finishing chapter N queues chapter N+1.
- ETA: remaining tokens / rolling average tok/s, per scene and per chapter.
- Thermal aware: the guard's ThermalGate runs between scenes.

Run:
    python -m noirwrit.worker --db ~/.noirwrit/noirwrit.db
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import signal
import socket
import sys
import threading
import time

import psutil

from noirwrit.config import HOME
from noirwrit.guardrails import ThermalGate, tree_rss_bytes
from noirwrit.memory.db import DB

STALE_S = 60.0
HEARTBEAT_S = 5.0
EMA_ALPHA = 0.2


def enqueue_chapter(db: DB, story_id: int, chapter: int, priority: int = 0) -> int | None:
    """Queue a chapter unless it is done or already queued/running."""
    ch = db.one("SELECT status FROM chapters WHERE story_id=? AND num=?", (story_id, chapter))
    if ch is None or ch["status"] == "done":
        return None
    payload = json.dumps({"story_id": story_id, "chapter": chapter})
    existing = db.one("SELECT id, priority FROM jobs WHERE kind='chapter' AND payload=? AND status IN ('queued','running')", (payload,))
    if existing:
        if priority < existing["priority"]:
            db.execute("UPDATE jobs SET priority=? WHERE id=?", (priority, existing["id"]))
        return int(existing["id"])
    db.execute("UPDATE chapters SET status='queued' WHERE story_id=? AND num=? AND status='pending'", (story_id, chapter))
    return int(db.execute("INSERT INTO jobs(created, kind, payload, priority) VALUES (?, 'chapter', ?, ?)",
                          (time.time(), payload, priority)).lastrowid)


def requeue_stale(db: DB, stale_s: float = STALE_S) -> int:
    cur = db.execute("UPDATE jobs SET status='queued', worker=NULL WHERE status='running' AND (heartbeat IS NULL OR heartbeat < ?)",
                     (time.time() - stale_s,))
    return cur.rowcount


def claim(db: DB, worker_id: str) -> dict | None:
    """Atomically claim the next job."""
    conn = db.conn
    with conn:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT id, kind, payload FROM jobs WHERE status='queued' ORDER BY priority, id LIMIT 1").fetchone()
        if row is None:
            return None
        conn.execute("UPDATE jobs SET status='running', worker=?, heartbeat=?, attempts=attempts+1 WHERE id=?",
                     (worker_id, time.time(), row["id"]))
    return {"id": row["id"], "kind": row["kind"], **json.loads(row["payload"])}


def tok_rate(db: DB) -> float:
    return float(db.get_setting("tok_per_s", 0.0) or 0.0)


def update_rate(db: DB, sample: float) -> float:
    if sample <= 0:
        return tok_rate(db)
    old = tok_rate(db)
    new = sample if old <= 0 else (1 - EMA_ALPHA) * old + EMA_ALPHA * sample
    db.set_setting("tok_per_s", new)
    return new


def remaining_tokens(db: DB, story_id: int, chapter: int | None = None) -> int:
    q = "SELECT beat, status, tokens FROM scenes WHERE story_id=?"
    args: list = [story_id]
    if chapter is not None:
        q += " AND chapter_num=?"
        args.append(chapter)
    total = 0
    for r in db.query(q, args):
        if r["status"] != "done":
            total += int(json.loads(r["beat"]).get("target_words", 500) * 1.35)
    return total


def eta_seconds(db: DB, story_id: int, chapter: int | None = None, in_progress_tokens: int = 0) -> float | None:
    rate = tok_rate(db)
    if rate <= 0:
        return None
    return max(remaining_tokens(db, story_id, chapter) - in_progress_tokens, 0) / rate


class Worker:
    def __init__(self, db: DB, engine_factory, worker_id: str | None = None, prefetch: bool = True,
                 thermal: ThermalGate | None = None, poll_s: float = 1.0):
        self.db = db
        self.engine_factory = engine_factory
        self.engine = None
        self.id = worker_id or f"{socket.gethostname()}:{os.getpid()}"
        self.prefetch = prefetch
        self.thermal = thermal or ThermalGate()
        self.poll_s = poll_s
        self._stop = threading.Event()
        self._job: dict | None = None
        self._live: dict = {}

    def stop(self) -> None:
        self._stop.set()

    def _heartbeat_loop(self) -> None:
        while not self._stop.is_set():
            job = self._job
            if job:
                DB(self.db.path).execute("UPDATE jobs SET heartbeat=?, progress=? WHERE id=?",
                                         (time.time(), json.dumps(self._live), job["id"]))
            self._stop.wait(HEARTBEAT_S)

    def _progress(self, ev: dict) -> None:
        if ev["event"] == "scene_start":
            self._live = {"chapter": ev["chapter"], "scene": ev["scene"], "of": ev["of"], "tokens": 0,
                          "target": ev["target_tokens"], "t0": time.time()}
        elif ev["event"] == "token":
            self._live["tokens"] = self._live.get("tokens", 0) + max(1, len(ev["text"]) // 4)
        elif ev["event"] == "scene_live" and self._job:
            # The reader streams this row and types it out.
            self.db.execute(
                "INSERT INTO live(story_id, chapter_num, scene_num, text, updated) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(story_id, chapter_num) DO UPDATE SET scene_num=excluded.scene_num, text=excluded.text, "
                "updated=excluded.updated",
                (self._job["story_id"], ev["chapter"], ev["scene"], ev["text"], time.time()))
        elif ev["event"] == "scene_done":
            if ev["seconds"] > 0:
                update_rate(self.db, ev["tokens"] / ev["seconds"])

    def _between_scenes(self) -> None:
        """Runs before every scene: thermal pause, then the RAM ceiling from Settings."""
        saved = self.db.get_setting("hot_pause_min")
        if saved:
            self.thermal.hot_pause_s = float(saved) * 60
        self.thermal.wait_if_hot()
        limit_gb = float(self.db.get_setting("max_rss_gb", 3) or 3)
        used = tree_rss_bytes(psutil.Process()) / 1024**3
        if used > limit_gb:
            # Drop the model and caches; the next scene reloads them. Saved scenes are safe.
            print(f"[worker] memory {used:.2f} GB over the {limit_gb} GB ceiling; reloading the engine", file=sys.stderr, flush=True)
            self.engine = None
            gc.collect()
            self.engine = self.engine_factory(self.db)

    def run_job(self, job: dict) -> None:
        if self.engine is None:
            self.engine = self.engine_factory(self.db)
        sid, ch = job["story_id"], job["chapter"]
        self._job = job
        try:
            self.engine.write_chapter(sid, ch, progress=self._progress, should_stop=self._stop.is_set,
                                      between_scenes=self._between_scenes)
            self.db.execute("UPDATE jobs SET status='done', heartbeat=? WHERE id=?", (time.time(), job["id"]))
            if self.prefetch:
                enqueue_chapter(self.db, sid, ch + 1, priority=1)
        except InterruptedError:
            self.db.execute("UPDATE jobs SET status='queued', worker=NULL WHERE id=?", (job["id"],))
        except Exception as e:
            self.db.execute("UPDATE jobs SET status='failed', error=? WHERE id=?", (repr(e)[:2000], job["id"]))
            self.db.execute("UPDATE chapters SET status='failed' WHERE story_id=? AND num=?", (sid, ch))
        finally:
            self._job = None
            self._live = {}

    def run(self, once: bool = False) -> None:
        requeue_stale(self.db)
        hb = threading.Thread(target=self._heartbeat_loop, daemon=True)
        hb.start()
        while not self._stop.is_set():
            job = claim(self.db, self.id)
            if job is None:
                if once:
                    break
                self._stop.wait(self.poll_s)
                continue
            self.run_job(job)
        self._stop.set()


def default_engine_factory(db: DB):
    """Story engine on the best available local model, at the quality chosen in Settings."""
    from noirwrit.memory.store import Memory
    from noirwrit.planner.story import StoryEngine
    from noirwrit.runtime.models import load_generator

    quality = db.get_setting("quality", "balanced") or "balanced"
    candidates = {"fast": 1, "balanced": 1, "quality": 3}.get(quality, 1)
    return StoryEngine(db, Memory(db), load_generator(db, quality=quality), candidates=candidates)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(HOME / "noirwrit.db"))
    ap.add_argument("--once", action="store_true", help="exit when the queue is empty")
    ap.add_argument("--stale-s", type=float, default=STALE_S, help="requeue running jobs with an older heartbeat")
    a = ap.parse_args(argv)
    db = DB(a.db)
    requeue_stale(db, a.stale_s)
    w = Worker(db, default_engine_factory)
    signal.signal(signal.SIGTERM, lambda *_: w.stop())
    try:
        w.run(once=a.once)
    except KeyboardInterrupt:
        w.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
