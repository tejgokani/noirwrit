import os
import signal
import subprocess
import sys
import time

import pytest

from noirwrit.memory.db import DB
from noirwrit.memory.embed import HashingEmbedder
from noirwrit.memory.store import Memory
from noirwrit.planner.generators import EchoGenerator
from noirwrit.planner.spec import Spec
from noirwrit.planner.story import StoryEngine, create_story
from noirwrit.worker import (
    Worker,
    claim,
    enqueue_chapter,
    eta_seconds,
    requeue_stale,
    tok_rate,
    update_rate,
)


def _wait(pred, timeout=60, step=0.1):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if pred():
            return True
        time.sleep(step)
    return False


def test_queue_claim_and_dedupe(tmp_path):
    db = DB(tmp_path / "q.db")
    sid = create_story(db, Spec(seed=1, chapters=3))
    a = enqueue_chapter(db, sid, 1)
    assert enqueue_chapter(db, sid, 1) == a  # no duplicate job
    enqueue_chapter(db, sid, 2, priority=1)
    job = claim(db, "w1")
    assert job["chapter"] == 1  # priority 0 first
    assert claim(db, "w2")["chapter"] == 2
    assert claim(db, "w3") is None


def test_stale_job_is_requeued(tmp_path):
    db = DB(tmp_path / "q.db")
    sid = create_story(db, Spec(seed=1, chapters=1))
    enqueue_chapter(db, sid, 1)
    claim(db, "dead-worker")
    db.execute("UPDATE jobs SET heartbeat=?", (time.time() - 3600,))
    assert requeue_stale(db) == 1
    assert claim(db, "w2") is not None


def test_kill_worker_mid_chapter_then_resume(tmp_path):
    """A SIGKILLed worker loses at most the scene in progress; a restarted worker finishes the chapter."""
    db_path = tmp_path / "w.db"
    db = DB(db_path)
    sid = create_story(db, Spec(seed=8, chapters=1, chapter_words=3000))
    total = db.one("SELECT COUNT(*) AS c FROM scenes WHERE story_id=?", (sid,))["c"]
    enqueue_chapter(db, sid, 1)
    env = {**os.environ, "NOIRWRIT_GENERATOR": "echo:900", "NOIRWRIT_HOME": str(tmp_path)}

    def done_scenes():
        return {r["num"]: r["text"] for r in DB(db_path).query(
            "SELECT num, text FROM scenes WHERE story_id=? AND status='done'", (sid,))}

    p = subprocess.Popen([sys.executable, "-m", "noirwrit.worker", "--db", str(db_path)], env=env)
    try:
        assert _wait(lambda: len(done_scenes()) >= 2, timeout=60)
        p.send_signal(signal.SIGKILL)
        p.wait(timeout=10)
    finally:
        if p.poll() is None:
            p.kill()
    before = done_scenes()
    assert 2 <= len(before) < total
    assert DB(db_path).one("SELECT status FROM jobs")["status"] == "running"  # left behind by the dead worker

    p2 = subprocess.Popen([sys.executable, "-m", "noirwrit.worker", "--db", str(db_path), "--stale-s", "0", "--once"], env=env)
    assert p2.wait(timeout=120) == 0
    after = done_scenes()
    assert len(after) == total
    for num, text in before.items():
        assert after[num] == text  # finished scenes were not rewritten
    assert DB(db_path).one("SELECT status FROM chapters WHERE story_id=?", (sid,))["status"] == "done"


def test_eta_within_20_percent(tmp_path):
    """Calibrate on chapter 1, predict chapter 2 from the rolling rate, then time it."""
    db = DB(tmp_path / "eta.db")
    sid = create_story(db, Spec(seed=2, chapters=2, chapter_words=2000))
    gen = EchoGenerator(tok_per_s=1500, simulate_speed=True)
    eng = StoryEngine(db, Memory(db, HashingEmbedder()), gen)
    w = Worker(db, lambda _db: eng, prefetch=False)
    w.thermal.thermal_fn = lambda: "nominal"
    enqueue_chapter(db, sid, 1)
    w.run(once=True)
    assert tok_rate(db) > 0
    predicted = eta_seconds(db, sid, 2)
    enqueue_chapter(db, sid, 2)
    t0 = time.time()
    w = Worker(db, lambda _db: eng, prefetch=False)
    w.thermal.thermal_fn = lambda: "nominal"
    w.run(once=True)
    actual = time.time() - t0
    assert abs(predicted - actual) / actual < 0.2, (predicted, actual)


def test_rate_is_a_rolling_average(tmp_path):
    db = DB(tmp_path / "r.db")
    update_rate(db, 100)
    assert tok_rate(db) == 100
    update_rate(db, 200)
    assert 100 < tok_rate(db) < 200


@pytest.mark.parametrize("hot,paused", [("serious", True), ("nominal", False)])
def test_worker_obeys_thermal_gate(tmp_path, hot, paused):
    db = DB(tmp_path / "t.db")
    sid = create_story(db, Spec(seed=3, chapters=1, chapter_words=1500))
    calls = []
    eng = StoryEngine(db, Memory(db, HashingEmbedder()), EchoGenerator())
    w = Worker(db, lambda _db: eng, prefetch=False)
    w.thermal.interval_s = 0
    w.thermal.hot_pause_s = 0.01
    w.thermal.thermal_fn = lambda: (calls.append(1), hot)[1]
    enqueue_chapter(db, sid, 1)
    w.run(once=True)
    assert calls  # checked between scenes
    assert db.one("SELECT status FROM chapters").__getitem__("status") == "done"
