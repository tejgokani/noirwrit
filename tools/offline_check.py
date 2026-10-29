#!/usr/bin/env python3
"""Run the full app flow with the network blocked and report every step.

    sandbox-exec -f tools/nonet.sb .venv/bin/python tools/offline_check.py

macOS sandbox-exec denies all outbound traffic except to localhost, for this
process and everything it starts (the server, the worker, llama.cpp, WeasyPrint).
Any step that needed the internet would fail here.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT = 8799
BASE = f"http://127.0.0.1:{PORT}"


def call(path: str, method: str = "GET", body: dict | None = None, raw: bool = False, timeout: float = 600):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = r.read()
        return (payload, r.headers.get("content-type", "")) if raw else json.loads(payload)


def internet_blocked() -> bool:
    try:
        socket.create_connection(("example.com", 443), timeout=5).close()
        return False
    except OSError:
        return True


def main() -> int:
    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}", flush=True)

    check("internet is unreachable from this process", internet_blocked())
    home = Path(tempfile.mkdtemp(prefix="noirwrit-offline-"))
    env = {**os.environ, "NOIRWRIT_HOME": str(home), "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
    models = home / "models"
    models.mkdir()
    gguf = ROOT / "artifacts" / "base" / "export" / "noirwrit-base-q8_0.gguf"
    srv = subprocess.Popen([sys.executable, "-m", "noirwrit.cli", "serve", "--no-browser", "--port", str(PORT)],
                           cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        for _ in range(120):
            try:
                st = call("/api/status")
                break
            except OSError:
                time.sleep(0.5)
        else:
            check("server starts", False, srv.stderr.read().decode()[-500:] if srv.poll() is not None else "timeout")
            return 1
        check("server starts on 127.0.0.1", True, f"model={Path(st['model']).name}")
        if gguf.exists():
            call("/api/settings", "POST", {"model_path": str(gguf)})

        page, ctype = call("/", raw=True)
        external = [u for u in __import__("re").findall(rb'(?:src|href)="([^"]+)"', page) if not u.startswith((b"/", b"#"))]
        check("page loads with no external resources", not external and b"Noirwrit" in page, f"{len(page)} bytes")

        sid = call("/api/stories", "POST", {"spec": {"chapters": 2, "chapter_words": 1500, "genre": "noir", "seed": 4321}})["story_id"]
        check("story planned", True, f"story {sid}")

        t0 = time.time()
        while time.time() - t0 < 300:
            s = call(f"/api/stories/{sid}")
            if s["chapters"][0]["status"] == "done":
                break
            time.sleep(1)
        ch = call(f"/api/stories/{sid}/chapters/1")
        check("chapter 1 written by the worker", ch["status"] == "done" and len(ch["text"].split()) > 800,
              f"{len(ch['text'].split())} words in {time.time() - t0:.0f} s")

        stream, ctype = call(f"/api/stories/{sid}/chapters/1/stream", raw=True, timeout=60)
        check("live stream sends scenes and ends", ctype.startswith("text/event-stream") and b"event: end" in stream,
              f"{stream.count(b'event: scene')} scene events")

        t0 = time.time()
        while time.time() - t0 < 300 and call(f"/api/stories/{sid}")["status"] != "done":
            time.sleep(1)
        check("prefetch writes chapter 2", call(f"/api/stories/{sid}")["status"] == "done")

        for fmt, magic in (("pdf", b"%PDF-"), ("epub", b"PK"), ("txt", b"CHAPTER"), ("md", b"# ")):
            data, ctype = call(f"/api/stories/{sid}/export?fmt={fmt}", raw=True)
            ok = data[:5].startswith(magic) or magic in data[:200]
            check(f"export {fmt}", ok, f"{len(data):,} bytes")

        r = urllib.request.Request(BASE + "/api/memory/ingest", data=b"text=The+ledger+is+in+the+cellar.&source=notes",
                                   method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(r) as resp:
            n = json.loads(resp.read())["chunks"]
        hits = call("/api/memory/search?q=where+is+the+ledger")["hits"]
        check("memory ingest and search", n == 1 and bool(hits) and "ledger" in hits[0]["text"])
        check("settings save", call("/api/settings", "POST", {"page_size": "A5"})["settings"]["page_size"] == "A5")
        check("internet still unreachable after the run", internet_blocked())
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=15)
        except subprocess.TimeoutExpired:
            srv.kill()
    failed = [n for n, ok, _ in results if not ok]
    print(json.dumps({"passed": len(results) - len(failed), "failed": failed, "home": str(home)}), flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
