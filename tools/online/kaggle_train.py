#!/usr/bin/env python3
"""Train Noirwrit on Kaggle's free GPUs, end to end, from this Mac.

Needs a Kaggle API token in ~/.kaggle/access_token (or the older ~/.kaggle/kaggle.json);
see docs/ONLINE_TRAINING.md. Then:
    python tools/online/kaggle_train.py            # upload, train, chain sessions, download, export
    python tools/online/kaggle_train.py --status   # show the current session

What it does:
  1. Uploads a private Kaggle dataset (noirwrit-data): the code as one tar file, the shards
     gzipped, and meta.json. Flat files only, so Kaggle's handling of folders does not matter.
  2. Pushes a private T4 GPU kernel (noirwrit-train-a). It probes the GPU, plans the run (base
     if at least one epoch fits, else small) and trains with 30-minute checkpoints.
  3. Polls every few minutes, downloading only status.json and the log. If a session ends before
     training finishes (Kaggle's 12 h limit), it pushes noirwrit-train-b with the first session's
     output attached; that session resumes from latest.pt on Kaggle's side. Then a, then b.
  4. When DONE.json appears, downloads only final-weights.pt (fp16, ~195 MB) to
     artifacts/<preset>/best.pt and exports GGUF Q8_0 and Q4_K_M.
Cost: $0. Kaggle grants about 30 GPU hours a week.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "artifacts" / "kaggle"
LOG = ROOT / "logs" / "online.log"
ACCELERATOR = "NvidiaTeslaT4"
SMALL_FILES = r"^(status\.json|DONE\.json|train_log\.jsonl|plan\.(json|txt))$"


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def kaggle_exe() -> str:
    local = Path(sys.executable).parent / "kaggle"
    return str(local) if local.exists() else (shutil.which("kaggle") or "kaggle")


def kaggle(*args: str, check: bool = True, timeout: int = 7200) -> str:
    r = subprocess.run([kaggle_exe(), *args], capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"kaggle {' '.join(args[:2])} failed: {(r.stderr or r.stdout).strip()[-800:]}")
    return r.stdout + r.stderr


def username() -> str:
    home = Path.home() / ".kaggle"
    if not (home / "access_token").exists() and not (home / "kaggle.json").exists():
        sys.exit("No Kaggle token. Follow the steps in docs/ONLINE_TRAINING.md.")
    for name in ("access_token", "kaggle.json"):
        p = home / name
        if p.exists() and p.stat().st_mode & 0o077:
            p.chmod(0o600)
    if (home / "kaggle.json").exists():
        return json.loads((home / "kaggle.json").read_text())["username"]
    m = re.search(r"username:\s*(\S+)", kaggle("config", "view", check=False))
    if not m or m.group(1) == "None":
        sys.exit("Could not read the Kaggle username; run `kaggle config view`.")
    return m.group(1)


def build_dataset(user: str) -> Path:
    d = WORK / "dataset"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    with tarfile.open(d / "noirwrit_code.tar", "w") as t:
        t.add(ROOT / "noirwrit", "noirwrit",
              filter=lambda i: None if "__pycache__" in i.name or i.name.endswith(".pyc") or "/static" in i.name else i)
    shards = ROOT / "data" / "shards"
    shutil.copy(shards / "meta.json", d / "meta.json")
    for f in sorted(shards.glob("*.bin")):
        with open(f, "rb") as fi, gzip.open(d / (f.name + ".gz"), "wb", compresslevel=6) as fo:
            shutil.copyfileobj(fi, fo, 1 << 24)
    (d / "dataset-metadata.json").write_text(json.dumps({
        "title": "noirwrit-data", "id": f"{user}/noirwrit-data",
        "licenses": [{"name": "CC0-1.0"}],
    }, indent=2))
    return d


def dataset_exists(user: str) -> bool:
    out = kaggle("datasets", "list", "--mine", "-s", "noirwrit-data", check=False)
    return f"{user}/noirwrit-data" in out


def push_dataset(user: str) -> None:
    d = build_dataset(user)
    size = sum(f.stat().st_size for f in d.iterdir() if f.is_file()) / 1e6
    exists = dataset_exists(user)
    log(f"uploading dataset noirwrit-data ({size:.0f} MB, {'new version' if exists else 'new, private'})")
    t0 = time.time()
    if exists:
        kaggle("datasets", "version", "-p", str(d), "-m", f"update {time.strftime('%Y-%m-%d %H:%M')}", "-r", "skip")
    else:
        kaggle("datasets", "create", "-p", str(d), "-r", "skip")
    log(f"upload finished in {(time.time() - t0) / 60:.1f} min; waiting for Kaggle to process it")
    for _ in range(90):
        st = kaggle("datasets", "status", f"{user}/noirwrit-data", check=False).strip().lower()
        if "ready" in st:
            log("dataset ready")
            return
        time.sleep(20)
    log("dataset still processing after 30 minutes; continuing anyway")


def push_kernel(user: str, slug: str, resume_from: str | None) -> None:
    d = WORK / slug
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "online" / "kaggle_kernel.py", d / "kaggle_kernel.py")
    meta = {
        "id": f"{user}/{slug}", "title": slug, "code_file": "kaggle_kernel.py", "language": "python",
        "kernel_type": "script", "is_private": "true", "enable_gpu": "true", "enable_tpu": "false",
        "enable_internet": "false", "machine_shape": ACCELERATOR,
        "dataset_sources": [f"{user}/noirwrit-data"], "kernel_sources": [resume_from] if resume_from else [],
        "competition_sources": [], "model_sources": [],
    }
    (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
    out = kaggle("kernels", "push", "-p", str(d), "--accelerator", ACCELERATOR)
    log(f"pushed {slug}{' (resumes from ' + resume_from + ')' if resume_from else ''}: {out.strip()[-300:]}")


def status(ref: str) -> str:
    out = kaggle("kernels", "status", ref, check=False).lower()
    for s in ("complete", "error", "cancel", "running", "queued"):
        if s in out:
            return s
    return "unknown"


def fetch(ref: str, dest: Path, pattern: str) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    kaggle("kernels", "output", ref, "-p", str(dest), "--file-pattern", pattern, "-o", "-q")
    return dest


def finish(ref: str, out: Path) -> None:
    done = json.loads((out / "DONE.json").read_text())
    preset = done["plan"]["preset"]
    log(f"training finished ({preset}, best val {done.get('best_val')}); downloading final weights")
    fetch(ref, out, r"^final-weights\.pt$")
    target = ROOT / "artifacts" / preset
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy(out / "final-weights.pt", target / "best.pt")
    for name in ("train_log.jsonl", "plan.txt", "plan.json", "DONE.json", "status.json"):
        if (out / name).exists():
            shutil.copy(out / name, target / name)
    py = sys.executable
    subprocess.run([py, "-m", "noirwrit.runtime.export", str(target / "best.pt"), "--out-dir", str(target / "export"),
                    "--name", f"noirwrit-{preset}", "--gguf", "--quant", "Q8_0"], check=True, cwd=ROOT)
    f32 = target / "export" / f"noirwrit-{preset}-f32.gguf"
    subprocess.run([shutil.which("llama-quantize") or "llama-quantize", str(f32),
                    str(target / "export" / f"noirwrit-{preset}-q4_k_m.gguf"), "Q4_K_M"], capture_output=True)
    f32.unlink(missing_ok=True)
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

    def save() -> None:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state, indent=2))

    if a.status:
        print(json.dumps(state, indent=2))
        if state.get("current"):
            ref = state["current"]
            print(ref, status(ref))
            st = fetch(ref, WORK / "peek", r"^status\.json$") / "status.json"
            if st.exists():
                print(st.read_text())
        return 0

    if not a.skip_upload and not state.get("uploaded"):
        push_dataset(user)
        state["uploaded"] = True
        save()

    while state["session"] < a.max_sessions:
        if state.get("current") is None:
            slug = "noirwrit-train-a" if state["session"] % 2 == 0 else "noirwrit-train-b"
            push_kernel(user, slug, state.get("previous"))
            state["current"] = f"{user}/{slug}"
            save()
        ref = state["current"]
        st = status(ref)
        while st in ("running", "queued", "unknown"):
            time.sleep(a.poll_min * 60)
            st = status(ref)
            peek = fetch(ref, WORK / "peek", r"^status\.json$") / "status.json" if st == "running" else None
            info = json.loads(peek.read_text()) if peek and peek.exists() else {}
            log(f"{ref}: {st} {info.get('state', '')} step {info.get('step', '?')}")
        out = fetch(ref, WORK / f"out-{state['session']}", SMALL_FILES)
        if (out / "DONE.json").exists():
            finish(ref, out)
            state.update(current=None, done=True)
            save()
            return 0
        sj = out / "status.json"
        info = json.loads(sj.read_text()) if sj.exists() else {}
        if st != "complete" or info.get("state") == "error":
            log(f"{ref} ended with status {st}: {info.get('error', 'see the log on kaggle.com')}")
            return 1
        state.update(session=state["session"] + 1, previous=ref, current=None)
        save()
        log(f"session {state['session']} ended at step {info.get('step')} of {info.get('total_steps')}; chaining the next one")
    log("reached --max-sessions without finishing; rerun to continue")
    return 1


if __name__ == "__main__":
    sys.exit(main())
