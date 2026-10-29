"""Local web app: FastAPI on 127.0.0.1, one offline page, a separate worker process.

Screens (all in static/index.html): New story, Reader, Library, Memory, Settings.
No network calls: no CDNs, no fonts from the web, no telemetry.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from noirwrit import __version__
from noirwrit.config import HOME, load_requirements
from noirwrit.export import books as ex
from noirwrit.memory.db import DB
from noirwrit.memory.store import Memory, match_spec
from noirwrit.planner.spec import QUESTIONS, Spec
from noirwrit.planner.story import create_story, load_story
from noirwrit.runtime.models import list_models, pick_model
from noirwrit.worker import enqueue_chapter, eta_seconds, tok_rate

STATIC = Path(__file__).parent / "static"
EXPORTS = HOME / "exports"

DEFAULT_SETTINGS = {
    "quality": "balanced",  # fast | balanced | quality
    "model_path": None,
    "prefetch": True,
    "hot_pause_min": 4,
    "max_rss_gb": 3,
    "page_size": "6x9",
    "font_size_pt": 11,
    "include_cover": True,
    "include_toc": True,
    "kindle_folder": str(Path.home() / "Desktop"),
}


class State:
    db: DB
    mem: Memory
    worker: subprocess.Popen | None = None
    db_path: str


S = State()


def settings() -> dict:
    out = dict(DEFAULT_SETTINGS)
    for k in DEFAULT_SETTINGS:
        v = S.db.get_setting(k)
        if v is not None:
            out[k] = v
    return out


def start_worker() -> None:
    if os.environ.get("NOIRWRIT_NO_WORKER"):
        return
    if S.worker and S.worker.poll() is None:
        return
    S.worker = subprocess.Popen([sys.executable, "-m", "noirwrit.worker", "--db", S.db_path],
                                stdout=subprocess.DEVNULL, stderr=open(HOME / "worker.log", "a"))


def stop_worker() -> None:
    if S.worker and S.worker.poll() is None:
        S.worker.terminate()
        try:
            S.worker.wait(timeout=10)
        except subprocess.TimeoutExpired:
            S.worker.kill()


@asynccontextmanager
async def lifespan(app: FastAPI):
    HOME.mkdir(parents=True, exist_ok=True)
    S.db_path = os.environ.get("NOIRWRIT_DB", str(HOME / "noirwrit.db"))
    S.db = DB(S.db_path)
    S.mem = Memory(S.db)
    start_worker()
    yield
    stop_worker()


app = FastAPI(title="Noirwrit", version=__version__, lifespan=lifespan, docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (STATIC / "index.html").read_text()


# New story ----------------------------------------------------------------

@app.get("/api/questions")
def questions():
    req = load_requirements()
    defaults = req.get("generation_defaults", {})
    qs = [dict(q) for q in QUESTIONS]
    for q in qs:
        if q["key"] == "chapter_words":
            q["default"] = defaults.get("chapter_words", q.get("default"))
    return {"questions": qs, "genre_mix": defaults.get("genre_mix", {})}


class SpecIn(BaseModel):
    spec: dict
    mode: str = "fresh"  # fresh | continue | vary
    match_spec_id: int | None = None


@app.post("/api/match")
def api_match(body: SpecIn):
    m = match_spec({k: v for k, v in body.spec.items() if v not in ("", None)}, S.db.requested_specs(), S.mem.emb)
    if not m:
        return {"match": None}
    story = S.db.one("SELECT id, title, status FROM stories WHERE spec_id=? ORDER BY id DESC LIMIT 1", (m["spec_id"],))
    return {"match": {**m, "story": dict(story) if story else None}}


@app.post("/api/stories")
def api_create(body: SpecIn):
    spec = dict(body.spec)
    parent = None
    if body.mode in ("continue", "vary") and body.match_spec_id:
        row = S.db.one("SELECT id FROM stories WHERE spec_id=? ORDER BY id DESC LIMIT 1", (body.match_spec_id,))
        if row and body.mode == "continue":
            nxt = S.db.one("SELECT MIN(num) AS n FROM chapters WHERE story_id=? AND status!='done'", (row["id"],))
            if nxt and nxt["n"]:
                enqueue_chapter(S.db, row["id"], nxt["n"], priority=0)
            return {"story_id": row["id"], "mode": "continue"}
        parent = row["id"] if row else None
    spec.setdefault("seed", int(time.time()) % 100000)
    if body.mode == "vary":
        spec["seed"] = (int(spec["seed"]) + 7919) % 100000
        # A variation keeps the request but lets the planner pick fresh specifics.
        for k in ("culprit", "motive", "twist", "detective_name"):
            spec.pop(k, None)
    clean = {k: v for k, v in spec.items() if v not in ("", None)}
    sid = create_story(S.db, Spec.from_dict(clean), raw_request=json.dumps(body.spec), parent_story_id=parent)
    enqueue_chapter(S.db, sid, 1, priority=0)
    start_worker()
    return {"story_id": sid, "mode": body.mode}


# Library and reader -------------------------------------------------------

@app.get("/api/stories")
def api_stories():
    rows = S.db.query(
        "SELECT s.id, s.title, s.status, s.created, s.parent_story_id, "
        "(SELECT COUNT(*) FROM chapters c WHERE c.story_id=s.id) AS chapters, "
        "(SELECT COUNT(*) FROM chapters c WHERE c.story_id=s.id AND c.status='done') AS done, "
        "(SELECT COALESCE(SUM(words),0) FROM chapters c WHERE c.story_id=s.id) AS words "
        "FROM stories s ORDER BY s.id DESC")
    return {"stories": [dict(r) for r in rows]}


def _chapter_state(story_id: int, num: int) -> dict:
    ch = S.db.one("SELECT num, title, status, words, updated FROM chapters WHERE story_id=? AND num=?", (story_id, num))
    if ch is None:
        raise HTTPException(404, "chapter not found")
    scenes = S.db.query("SELECT num, status, tokens, beat FROM scenes WHERE story_id=? AND chapter_num=? ORDER BY num",
                        (story_id, num))
    live = _live_job(story_id, num)
    in_prog = live.get("tokens", 0) if live else 0
    eta = None if ch["status"] == "done" else eta_seconds(S.db, story_id, num, in_prog)
    total_target = sum(int(json.loads(s["beat"]).get("target_words", 500) * 1.35) for s in scenes) or 1
    done_tok = sum(int(json.loads(s["beat"]).get("target_words", 500) * 1.35) for s in scenes if s["status"] == "done")
    pct = 100.0 if ch["status"] == "done" else min(99.0, 100.0 * (done_tok + in_prog) / total_target)
    return {**dict(ch), "eta_s": eta, "percent": round(pct, 1),
            "scenes": [{"num": s["num"], "status": s["status"], "kind": json.loads(s["beat"]).get("kind")} for s in scenes],
            "live": live}


def _live_job(story_id: int, num: int) -> dict | None:
    payload = json.dumps({"story_id": story_id, "chapter": num})
    j = S.db.one("SELECT status, progress, heartbeat FROM jobs WHERE kind='chapter' AND payload=? ORDER BY id DESC LIMIT 1", (payload,))
    if not j:
        return None
    prog = json.loads(j["progress"]) if j["progress"] else {}
    return {"job_status": j["status"], **prog}


@app.get("/api/stories/{story_id}")
def api_story(story_id: int):
    try:
        info, spec, outline = load_story(S.db, story_id)
    except KeyError as e:
        raise HTTPException(404, str(e)) from e
    chapters = [_chapter_state(story_id, ch["num"]) for ch in outline.chapters]
    remaining = eta_seconds(S.db, story_id)
    return {"id": story_id, "title": info["title"], "status": info["status"], "spec": spec.__dict__,
            "chapters": chapters, "eta_story_s": remaining, "tok_per_s": round(tok_rate(S.db), 1)}


@app.get("/api/stories/{story_id}/chapters/{num}")
def api_chapter(story_id: int, num: int):
    st = _chapter_state(story_id, num)
    row = S.db.one("SELECT text FROM chapters WHERE story_id=? AND num=?", (story_id, num))
    text = row["text"] if row and row["text"] else ""
    if not text:
        # Show finished scenes while the chapter is still being written.
        text = "\n\n".join(r["text"] for r in S.db.query(
            "SELECT text FROM scenes WHERE story_id=? AND chapter_num=? AND status='done' ORDER BY num", (story_id, num)))
    if settings()["prefetch"] and st["status"] == "done":
        enqueue_chapter(S.db, story_id, num + 1, priority=1)
    return {**st, "text": text}


@app.get("/api/stories/{story_id}/chapters/{num}/stream")
async def api_stream(story_id: int, num: int):
    """Server-Sent Events: each scene's text as it grows, then the final text, then 'end'.

    Events: scene {num, text, final}, status {status, percent, eta_s, live}, end {}.
    The reader diffs each scene against what it has typed so far.
    """
    import asyncio

    def sse(event: str, data: dict) -> str:
        return f"event: {event}\ndata: {json.dumps(data)}\n\n"

    async def gen():
        sent: dict[int, tuple[str, bool]] = {}
        last_status = 0.0
        idle_since = time.time()
        while True:
            ch = S.db.one("SELECT status FROM chapters WHERE story_id=? AND num=?", (story_id, num))
            if ch is None:
                yield sse("end", {"reason": "missing"})
                return
            changed = False
            for r in S.db.query("SELECT num, text FROM scenes WHERE story_id=? AND chapter_num=? AND status='done' "
                                "ORDER BY num", (story_id, num)):
                if sent.get(r["num"]) != (r["text"], True):
                    sent[r["num"]] = (r["text"], True)
                    changed = True
                    yield sse("scene", {"num": r["num"], "text": r["text"], "final": True})
            live = S.db.one("SELECT scene_num, text FROM live WHERE story_id=? AND chapter_num=?", (story_id, num))
            if live and not sent.get(live["scene_num"], ("", False))[1] and sent.get(live["scene_num"]) != (live["text"], False):
                sent[live["scene_num"]] = (live["text"], False)
                changed = True
                yield sse("scene", {"num": live["scene_num"], "text": live["text"], "final": False})
            now = time.time()
            if now - last_status >= 1.0:
                last_status = now
                st = _chapter_state(story_id, num)
                yield sse("status", {k: st[k] for k in ("status", "percent", "eta_s", "live")})
            if ch["status"] == "done":
                yield sse("end", {"reason": "done"})
                return
            idle_since = now if changed else idle_since
            if now - idle_since > 600:  # nothing for 10 minutes: let the client reconnect
                yield sse("end", {"reason": "idle"})
                return
            await asyncio.sleep(0.1)

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/stories/{story_id}/chapters/{num}/generate")
def api_generate(story_id: int, num: int):
    jid = enqueue_chapter(S.db, story_id, num, priority=0)
    start_worker()
    return {"job_id": jid}


@app.delete("/api/stories/{story_id}")
def api_delete(story_id: int):
    S.db.execute("DELETE FROM stories WHERE id=?", (story_id,))
    S.mem._invalidate()
    return {"ok": True}


# Status -------------------------------------------------------------------

@app.get("/api/status")
def api_status():
    q = {r["status"]: r["n"] for r in S.db.query("SELECT status, COUNT(*) AS n FROM jobs GROUP BY status")}
    running = S.db.one("SELECT payload, progress, heartbeat FROM jobs WHERE status='running' ORDER BY id LIMIT 1")
    alive = bool(S.worker and S.worker.poll() is None) or bool(running and running["heartbeat"] and time.time() - running["heartbeat"] < 30)
    pick = pick_model(S.db)
    return {"version": __version__, "worker_alive": alive, "queue": q, "tok_per_s": round(tok_rate(S.db), 1),
            "running": ({**json.loads(running["payload"]), **(json.loads(running["progress"]) if running["progress"] else {})}
                        if running else None),
            "model": pick["path"] if pick else "echo (no model installed)",
            "embedder": S.mem.emb.name}


# Memory -------------------------------------------------------------------

@app.get("/api/memory")
def api_memory():
    stories = []
    for s in S.db.query("SELECT id, title FROM stories ORDER BY id DESC"):
        ents = S.db.query("SELECT kind, name, data FROM bible_entities WHERE story_id=? AND kind IN ('character','clue')", (s["id"],))
        sums = S.db.query("SELECT chapter_num, text FROM summaries WHERE story_id=? ORDER BY chapter_num", (s["id"],))
        stories.append({
            "id": s["id"], "title": s["title"],
            "characters": [{"name": e["name"], **json.loads(e["data"])} for e in ents if e["kind"] == "character"],
            "clues": [{"id": e["name"], **json.loads(e["data"])} for e in ents if e["kind"] == "clue"],
            "summaries": [dict(r) for r in sums],
        })
    sources = S.db.query("SELECT source, COUNT(*) AS chunks, MIN(kind) AS kind FROM chunks WHERE story_id IS NULL GROUP BY source ORDER BY source")
    counts = S.db.one("SELECT COUNT(*) AS chunks FROM chunks")
    return {"stories": stories, "context_sources": [dict(r) for r in sources], "total_chunks": counts["chunks"],
            "names_used": S.db.one("SELECT COUNT(DISTINCT name) AS n FROM names_used")["n"]}


@app.post("/api/memory/ingest")
async def api_ingest(text: str = Form(""), source: str = Form("pasted text"), file: UploadFile | None = File(None)):
    n = 0
    if file is not None and file.filename:
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)
        try:
            renamed = tmp_path.with_name(Path(file.filename).name)
            tmp_path.rename(renamed)
            n += S.mem.ingest_file(renamed)
            renamed.unlink(missing_ok=True)
        except ValueError as e:
            raise HTTPException(400, str(e)) from e
    if text.strip():
        n += S.mem.ingest_text(text, source=source or "pasted text")
    return {"chunks": n}


@app.delete("/api/memory/sources/{source}")
def api_forget(source: str):
    S.db.execute("DELETE FROM chunks WHERE source=? AND story_id IS NULL", (source,))
    S.mem._invalidate()
    return {"ok": True}


@app.get("/api/memory/search")
def api_search(q: str, k: int = 5):
    return {"hits": [h.__dict__ for h in S.mem.search(q, k=k)]}


# Settings -----------------------------------------------------------------

@app.get("/api/settings")
def api_settings():
    return {"settings": settings(), "models": list_models()}


@app.post("/api/settings")
def api_set(body: dict):
    for k, v in body.items():
        if k in DEFAULT_SETTINGS:
            S.db.set_setting(k, v)
    # A new model or quality level takes effect on the next worker start.
    if {"model_path", "quality"} & set(body):
        stop_worker()
        start_worker()
    return {"settings": settings()}


# Export -------------------------------------------------------------------

def _book(story_id: int, chapter: int | None) -> ex.Book:
    info, spec, outline = load_story(S.db, story_id)
    q = "SELECT num, title, text FROM chapters WHERE story_id=? AND status='done'"
    args: list = [story_id]
    if chapter:
        q += " AND num=?"
        args.append(chapter)
    rows = S.db.query(q + " ORDER BY num", args)
    if not rows:
        raise HTTPException(400, "no finished chapters to export yet")
    title = info["title"] if not chapter else f"{info['title']}: Chapter {chapter}"
    return ex.Book(title=title, chapters=[(r["title"], r["text"]) for r in rows], language="en")


def _opts(page_size: str | None, font_size: float | None) -> ex.ExportOptions:
    st = settings()
    return ex.ExportOptions(page_size=page_size or st["page_size"], font_size_pt=float(font_size or st["font_size_pt"]),
                            include_cover=bool(st["include_cover"]), include_toc=bool(st["include_toc"]))


def _fname(book: ex.Book, ext: str) -> str:
    import re

    return (re.sub(r"[^A-Za-z0-9 _-]+", "", book.title).strip().replace(" ", "_") or "noirwrit") + "." + ext


@app.get("/api/stories/{story_id}/export")
def api_export(story_id: int, fmt: str = "pdf", chapter: int | None = None, page_size: str | None = None,
               font_size: float | None = None):
    book = _book(story_id, chapter)
    EXPORTS.mkdir(parents=True, exist_ok=True)
    name = _fname(book, fmt)
    out = EXPORTS / name
    if fmt == "txt":
        return PlainTextResponse(ex.to_txt(book), headers={"Content-Disposition": f'attachment; filename="{name}"'})
    if fmt == "md":
        return PlainTextResponse(ex.to_md(book), media_type="text/markdown",
                                 headers={"Content-Disposition": f'attachment; filename="{name}"'})
    if fmt == "pdf":
        ex.to_pdf(book, out, _opts(page_size, font_size))
        return FileResponse(out, media_type="application/pdf", filename=name)
    if fmt == "epub":
        ex.to_epub(book, out, _opts(page_size, font_size))
        return FileResponse(out, media_type="application/epub+zip", filename=name)
    raise HTTPException(400, f"unknown format {fmt}")


@app.post("/api/stories/{story_id}/print")
def api_print(story_id: int, chapter: int | None = None, page_size: str | None = None):
    book = _book(story_id, chapter)
    out = EXPORTS / _fname(book, "pdf")
    ex.to_pdf(book, out, _opts(page_size, None))
    ex.open_print_dialog(out)
    return {"path": str(out)}


class KindleIn(BaseModel):
    folder: str | None = None
    chapter: int | None = None


@app.post("/api/stories/{story_id}/kindle")
def api_kindle(story_id: int, body: KindleIn):
    book = _book(story_id, body.chapter)
    folder = Path(body.folder or settings()["kindle_folder"]).expanduser()
    res = ex.save_for_kindle(book, folder, _opts(None, None))
    check = ex.epubcheck(Path(res["path"]))
    res["epubcheck"] = None if check is None else {"ok": check[0]}
    return JSONResponse(res)


def serve(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> None:
    import threading
    import webbrowser

    import uvicorn

    if open_browser:
        threading.Timer(1.2, lambda: webbrowser.open(f"http://{host}:{port}/")).start()
    uvicorn.run(app, host=host, port=port, log_level="warning")
