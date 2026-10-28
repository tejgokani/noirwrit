#!/usr/bin/env python3
"""Train Noirwrit on Kaggle's free GPUs, end to end, from this Mac.

Needs ~/.kaggle/kaggle.json (see docs/ONLINE_TRAINING.md). Then:
    python tools/online/kaggle_train.py            # upload, train, chain sessions, download, export
    python tools/online/kaggle_train.py --status   # show the current session

What it does:
  1. Bundles code, tokenizer and shards into a private Kaggle dataset (noirwrit-data).
  2. Pushes a private GPU kernel (noirwrit-train-a) that probes the GPU, plans the run
     (base if it fits, else small) and trains with 30-minute checkpoints.
  3. Polls every few minutes. When a session ends before training finishes (Kaggle's
     12 h limit), it pushes the other kernel (noirwrit-train-b) with the first one's
     output attached, which resumes from latest.pt. Then a, then b, until DONE.json.
  4. Downloads the final checkpoints to artifacts/<preset>/ and exports GGUF.
Cost: $0. Kaggle grants about 30 GPU hours a week.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "artifacts" / "kaggle"
LOG = ROOT / "logs" / "online.log"


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def kaggle(*args: str, check: bool = True) -> str:
    exe = shutil.which("kaggle") or str(Path(sys.executable).parent / "kaggle")
    r = subprocess.run([exe, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"kaggle {' '.join(args)} failed: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def username() -> str:
    cred = Path.home() / ".kaggle" / "kaggle.json"
    if not cred.exists():
        sys.exit("Missing ~/.kaggle/kaggle.json. Follow the three steps in docs/ONLINE_TRAINING.md.")
    if cred.stat().st_mode & 0o077:
        cred.chmod(0o600)
    return json.loads(cred.read_text())["username"]


def build_dataset(user: str) -> Path:
    d = WORK / "dataset"
    if d.exists():
        shutil.rmtree(d)
    (d / "shards").mkdir(parents=True)
    shutil.copytree(ROOT / "noirwrit", d / "noirwrit",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "static", "templates"))
    shards = ROOT / "data" / "shards"
    for f in shards.iterdir():
        shutil.copy(f, d / "shards" / f.name)
    (d / "dataset-metadata.json").write_text(json.dumps({
        "title": "noirwrit-data", "id": f"{user}/noirwrit-data",
        "licenses": [{"name": "CC0-1.0"}],
        "description": "Tokenized public domain crime and detective fiction (Project Gutenberg, published 1930 or earlier) and Noirwrit training code.",
    }, indent=2))
    return d


def push_dataset(user: str) -> None:
    d = build_dataset(user)
    size = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) / 1e6
    exists = subprocess.run([shutil.which("kaggle") or "kaggle", "datasets", "status", f"{user}/noirwrit-data"],
                            capture_output=True, text=True).returncode == 0
    log(f"uploading dataset ({size:.0f} MB, {'new version' if exists else 'new'})")
    if exists:
        kaggle("datasets", "version", "-p", str(d), "-m", f"update {time.strftime('%Y-%m-%d %H:%M')}", "--dir-mode", "zip")
    else:
        kaggle("datasets", "create", "-p", str(d), "--dir-mode", "zip")
    # Wait until Kaggle has processed it, or the kernel will not see the files.
    for _ in range(60):
        st = kaggle("datasets", "status", f"{user}/noirwrit-data", check=False).strip().lower()
        if "ready" in st:
            return
        time.sleep(20)
    log("dataset still processing after 20 minutes; continuing anyway")


def push_kernel(user: str, slug: str, resume_from: str | None) -> None:
    d = WORK / slug
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "online" / "kaggle_kernel.py", d / "kaggle_kernel.py")
    meta = {
        "id": f"{user}/{slug}", "title": slug, "code_file": "kaggle_kernel.py", "language": "python",
        "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": False,
        "dataset_sources": [f"{user}/noirwrit-data"], "kernel_sources": [resume_from] if resume_from else [],
        "competition_sources": [],
    }
    (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
    out = kaggle("kernels", "push", "-p", str(d))
    log(f"pushed {slug}{' resuming from ' + resume_from if resume_from else ''}: {out.strip()}")


def status(ref: str) -> str:
    out = kaggle("kernels", "status", ref, check=False).lower()
    for s in ("complete", "error", "cancel", "running", "queued"):
        if s in out:
            return s
    return out.strip() or "unknown"


def download(ref: str, dest: Path) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    kaggle("kernels", "output", ref, "-p", str(dest))
    return dest


def finish(out: Path) -> None:
    done = json.loads((out / "DONE.json").read_text())
    preset = done["plan"]["preset"]
    target = ROOT / "artifacts" / preset
    target.mkdir(parents=True, exist_ok=True)
    for name in ("latest.pt", "best.pt", "train_log.jsonl", "plan.txt", "plan.json", "DONE.json"):
        if (out / name).exists():
            shutil.copy(out / name, target / name)
    log(f"training done: {preset}, best val {done.get('best_val')}; exporting")
    ck = target / ("best.pt" if (target / "best.pt").exists() else "latest.pt")
    subprocess.run([sys.executable, "-m", "noirwrit.runtime.export", str(ck), "--out-dir", str(target / "export"),
                    "--name", f"noirwrit-{preset}", "--gguf", "--quant", "Q8_0"], check=True, cwd=ROOT)
    subprocess.run([shutil.which("llama-quantize") or "llama-quantize", str(target / "export" / f"noirwrit-{preset}-f32.gguf"),
                    str(target / "export" / f"noirwrit-{preset}-q4_k_m.gguf"), "Q4_K_M"], capture_output=True)
    log(f"exported to {target / 'export'}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--skip-upload", action="store_true", help="reuse the dataset already on Kaggle")
    ap.add_argument("--poll-min", type=float, default=5.0)
    ap.add_argument("--max-sessions", type=int, default=4)
    a = ap.parse_args()
    user = username()
    state_file = WORK / "state.json"
    state = json.loads(state_file.read_text()) if state_file.exists() else {"session": 0, "current": None}

    if a.status:
        print(json.dumps(state, indent=2))
        if state["current"]:
            print(state["current"], status(state["current"]))
        return 0

    if not a.skip_upload and state["session"] == 0:
        push_dataset(user)

    while state["session"] < a.max_sessions:
        if state["current"] is None:
            slug = "noirwrit-train-a" if state["session"] % 2 == 0 else "noirwrit-train-b"
            prev = state.get("previous")
            push_kernel(user, slug, prev)
            state["current"] = f"{user}/{slug}"
            state_file.parent.mkdir(parents=True, exist_ok=True)
            state_file.write_text(json.dumps(state, indent=2))
        ref = state["current"]
        st = status(ref)
        while st in ("running", "queued", "unknown"):
            time.sleep(a.poll_min * 60)
            st = status(ref)
            log(f"{ref}: {st}")
        out = download(ref, WORK / f"out-{state['session']}")
        if (out / "DONE.json").exists():
            finish(out)
            state.update(current=None, done=True)
            state_file.write_text(json.dumps(state, indent=2))
            return 0
        if not (out / "latest.pt").exists():
            log(f"{ref} ended with status {st} and no checkpoint; see its log on kaggle.com")
            return 1
        state.update(session=state["session"] + 1, previous=ref, current=None)
        state_file.write_text(json.dumps(state, indent=2))
        log(f"session {state['session']} ended without finishing; chaining the next one")
    log("reached --max-sessions without finishing; rerun to continue")
    return 1


if __name__ == "__main__":
    sys.exit(main())
