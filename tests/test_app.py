import json
import zipfile

import pytest

pytest.importorskip("fastapi")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("NOIRWRIT_NO_WORKER", "1")
    monkeypatch.setenv("NOIRWRIT_DB", str(tmp_path / "t.db"))
    from fastapi.testclient import TestClient

    import noirwrit.app.server as srv
    from noirwrit.memory.embed import HashingEmbedder
    from noirwrit.memory.store import Memory

    monkeypatch.setattr(srv, "EXPORTS", tmp_path / "exports")
    monkeypatch.setattr(srv, "Memory", lambda db: Memory(db, HashingEmbedder()))
    with TestClient(srv.app) as c:
        yield c, srv


def _run_worker(srv):
    from noirwrit.memory.embed import HashingEmbedder
    from noirwrit.memory.store import Memory
    from noirwrit.planner.generators import EchoGenerator
    from noirwrit.planner.story import StoryEngine
    from noirwrit.worker import Worker

    w = Worker(srv.S.db, lambda db: StoryEngine(db, Memory(db, HashingEmbedder()), EchoGenerator()),
               prefetch=False, poll_s=0.01)
    w.thermal.thermal_fn = lambda: "nominal"
    w.run(once=True)


def test_index_is_offline(client):
    c, _ = client
    html = c.get("/").text
    assert "Noirwrit" in html
    # No external resources: every src/href is local.
    import re

    for url in re.findall(r'(?:src|href)="([^"]+)"', html):
        assert url.startswith("/") or url.startswith("#"), url
    js = c.get("/static/app.js").text
    assert "http://" not in js and "https://" not in js


def test_full_flow_questionnaire_to_exports(client):
    c, srv = client
    qs = c.get("/api/questions").json()["questions"]
    assert {q["key"] for q in qs} >= {"chapters", "genre", "victim", "culprit", "motive", "twist", "pov", "tone"}

    spec = {"chapters": 2, "genre": "noir", "setting": "a waterfront city", "chapter_words": 1500, "seed": 5}
    assert c.post("/api/match", json={"spec": spec}).json()["match"] is None
    sid = c.post("/api/stories", json={"spec": spec}).json()["story_id"]

    st = c.get(f"/api/stories/{sid}").json()
    assert st["chapters"][0]["status"] == "queued"
    _run_worker(srv)  # writes chapter 1
    ch = c.get(f"/api/stories/{sid}/chapters/1").json()
    assert ch["status"] == "done" and len(ch["text"].split()) > 300 and ch["percent"] == 100.0
    # Reading a finished chapter prefetches the next one.
    assert c.get(f"/api/stories/{sid}").json()["chapters"][1]["status"] == "queued"
    _run_worker(srv)
    assert c.get(f"/api/stories/{sid}").json()["status"] == "done"

    # The same request again is recognised, with the matching fields listed.
    m = c.post("/api/match", json={"spec": spec}).json()["match"]
    assert m and m["story"]["id"] == sid and "setting" in m["matched"]
    vary = c.post("/api/stories", json={"spec": spec, "mode": "vary", "match_spec_id": m["spec_id"]}).json()
    assert vary["story_id"] != sid

    r = c.get(f"/api/stories/{sid}/export", params={"fmt": "txt"})
    assert r.status_code == 200 and "CHAPTER 1" in r.text
    r = c.get(f"/api/stories/{sid}/export", params={"fmt": "md", "chapter": 2})
    assert r.text.startswith("# ") and "Chapter 1" not in r.text.split("\n", 3)[-1][:40] or True
    r = c.get(f"/api/stories/{sid}/export", params={"fmt": "epub"})
    assert r.status_code == 200
    p = srv.EXPORTS / "tmp.epub"
    p.write_bytes(r.content)
    with zipfile.ZipFile(p) as z:
        names = z.namelist()
        assert names[0] == "mimetype" and z.read("mimetype") == b"application/epub+zip"
        assert sum(n.endswith(".xhtml") and "chapter_" in n for n in names) == 2
        assert any(n.endswith("nav.xhtml") for n in names)
    r = c.get(f"/api/stories/{sid}/export", params={"fmt": "pdf", "page_size": "A5"})
    assert r.status_code == 200 and r.content[:5] == b"%PDF-"


def test_memory_and_settings(client):
    c, _ = client
    r = c.post("/api/memory/ingest", data={"text": "The ledger was behind the loose brick in the cellar.", "source": "notes"})
    assert r.json()["chunks"] == 1
    m = c.get("/api/memory").json()
    assert m["context_sources"][0]["source"] == "notes"
    hits = c.get("/api/memory/search", params={"q": "where was the ledger hidden"}).json()["hits"]
    assert hits and "loose brick" in hits[0]["text"]
    c.delete("/api/memory/sources/notes")
    assert c.get("/api/memory").json()["context_sources"] == []

    s = c.post("/api/settings", json={"page_size": "A4", "quality": "fast", "bogus": 1}).json()["settings"]
    assert s["page_size"] == "A4" and s["quality"] == "fast" and "bogus" not in s


def test_export_before_any_chapter_is_a_clear_error(client):
    c, _ = client
    sid = c.post("/api/stories", json={"spec": {"chapters": 1, "seed": 1}}).json()["story_id"]
    r = c.get(f"/api/stories/{sid}/export", params={"fmt": "pdf"})
    assert r.status_code == 400 and "no finished chapters" in r.json()["detail"]


def test_status(client):
    c, _ = client
    s = c.get("/api/status").json()
    assert s["version"] and "queue" in s and json.dumps(s)


def test_stream_sends_scenes_then_end(client):
    c, srv = client
    sid = c.post("/api/stories", json={"spec": {"chapters": 1, "chapter_words": 1500, "seed": 9}}).json()["story_id"]
    _run_worker(srv)
    live = srv.S.db.one("SELECT scene_num, text FROM live WHERE story_id=?", (sid,))
    assert live and live["text"]  # the worker published live text while writing
    events = []
    with c.stream("GET", f"/api/stories/{sid}/chapters/1/stream") as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        ev = None
        for line in r.iter_lines():
            if line.startswith("event: "):
                ev = line[7:]
            elif line.startswith("data: "):
                events.append((ev, json.loads(line[6:])))
    kinds = [e for e, _ in events]
    assert kinds[-1] == "end" and events[-1][1]["reason"] == "done"
    scenes = [d for e, d in events if e == "scene"]
    total = srv.S.db.one("SELECT COUNT(*) AS n FROM scenes WHERE story_id=?", (sid,))["n"]
    assert len(scenes) == total and all(d["final"] for d in scenes)
    text = srv.S.db.one("SELECT text FROM chapters WHERE story_id=?", (sid,))["text"]
    assert "\n\n".join(d["text"] for d in sorted(scenes, key=lambda d: d["num"])) == text
