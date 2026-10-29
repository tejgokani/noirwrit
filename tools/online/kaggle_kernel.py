"""Runs inside a Kaggle GPU session. Pushed by tools/online/kaggle_train.py; do not run locally.

Inputs (read-only, found by searching /kaggle/input, since Kaggle's mount layout varies):
  the noirwrit-data dataset: noirwrit_code.tar (or an extracted noirwrit/), shard files
  (*.bin or *.bin.gz) and meta.json
  the previous session's output, for resume: latest.pt, best.pt, train_log.jsonl, plan.json
Outputs (/kaggle/working):
  latest.pt, best.pt         full checkpoints, mounted by the next session to resume
  status.json                small progress file the launcher downloads
  final-weights.pt, DONE.json  written when training has finished (fp16 weights only, ~195 MB)
"""

import gzip
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

T0 = time.time()
SESSION_HOURS = 11.3  # Kaggle stops GPU sessions at 12 h; leave room to save
# NW_KAGGLE_ROOT lets the launcher's tests dry-run this script against a fake /kaggle tree.
KROOT = Path(os.environ.get("NW_KAGGLE_ROOT", "/kaggle"))
WORK = KROOT / "working"
INPUT = KROOT / "input"
TMP = Path(os.environ.get("NW_KAGGLE_TMP", "/tmp"))
SRC = TMP / "nw-src"
SHARDS = TMP / "nw-shards"
SETS = ("general", "crime", "noir")


def status(**kw):
    (WORK / "status.json").write_text(json.dumps({"t": time.time(), **kw}, indent=2))
    print("status:", kw, flush=True)


# 1. Find the dataset (meta.json marks it) and the previous session's output.
metas = [p for p in INPUT.rglob("meta.json") if "vocab_size" in p.read_text()[:200]]
if not metas:
    status(state="error", error="noirwrit-data dataset not attached")
    sys.exit(1)
data = metas[0].parent

# 2. Code: an extracted noirwrit/ package, or the tar archive.
SRC.mkdir(parents=True, exist_ok=True)
pkg = next(iter(INPUT.rglob("noirwrit/__init__.py")), None)
if pkg is not None:
    shutil.copytree(pkg.parent, SRC / "noirwrit", dirs_exist_ok=True)
else:
    tar = next(iter(INPUT.rglob("noirwrit_code.tar*")))
    with tarfile.open(tar) as t:
        t.extractall(SRC)
sys.path.insert(0, str(SRC))
os.environ["PYTHONPATH"] = str(SRC)

# 3. Shards: plain .bin files are used in place; gzipped ones are expanded to /tmp (not saved as output).
SHARDS.mkdir(parents=True, exist_ok=True)
shutil.copy(metas[0], SHARDS / "meta.json")
for s in SETS:
    for split in ("train", "val"):
        name = f"{s}_{split}.bin"
        plain = next(iter(INPUT.rglob(name)), None)
        if plain is not None:
            if not (SHARDS / name).exists():
                os.symlink(plain, SHARDS / name)
            continue
        gz = next(iter(INPUT.rglob(name + ".gz")))
        with gzip.open(gz, "rb") as fi, open(SHARDS / name, "wb") as fo:
            shutil.copyfileobj(fi, fo, 1 << 24)
print("shards:", sorted(p.name for p in SHARDS.iterdir()), flush=True)

# 4. Hugging Face Hub push, if the user added HF_TOKEN and HF_REPO secrets to the notebook.
try:
    from kaggle_secrets import UserSecretsClient

    sec = UserSecretsClient()
    os.environ["HF_TOKEN"] = sec.get_secret("HF_TOKEN")
    os.environ["HF_REPO"] = sec.get_secret("HF_REPO")
except Exception:
    pass

# 5. Resume from the newest checkpoint carried in from the previous session.
prev = sorted(INPUT.rglob("latest.pt"), key=lambda p: p.stat().st_mtime)
if prev:
    src = prev[-1].parent
    for name in ("latest.pt", "best.pt", "train_log.jsonl", "plan.json", "plan.txt"):
        if (src / name).exists() and not (WORK / name).exists():
            shutil.copy(src / name, WORK / name)
    print("resuming from", src, flush=True)

import torch  # noqa: E402

if not torch.cuda.is_available():
    status(state="error", error="no GPU in this session")
    sys.exit(1)
gpu = torch.cuda.get_device_name(0)
major, minor = torch.cuda.get_device_capability(0)
key = "t4" if "T4" in gpu else "p100" if "P100" in gpu else "a100" if "A100" in gpu else "l4" if "L4" in gpu else "t4"
print(f"GPU: {gpu} (sm{major}{minor}), torch {torch.__version__}", flush=True)
status(state="planning", gpu=gpu)

# 6. Plan once (2-minute probes per preset), then reuse the plan in later sessions.
MB, ACCUM = 16, 2  # 65k tokens per step
if (WORK / "plan.json").exists():
    plan = json.loads((WORK / "plan.json").read_text())
else:
    r = subprocess.run([sys.executable, "-m", "noirwrit.train.plan_run", "--gpu", key, "--shards", str(SHARDS),
                        "--budget-usd", "0", "--max-hours", "22", "--micro-batch", str(MB), "--accum", str(ACCUM),
                        "--probe", "--json", str(WORK / "plan.json")], capture_output=True, text=True)
    print(r.stdout, r.stderr[-4000:], flush=True)
    if r.returncode != 0:
        status(state="error", error="planning failed", stderr=r.stderr[-2000:])
        sys.exit(1)
    (WORK / "plan.txt").write_text(r.stdout)
    plan = json.loads((WORK / "plan.json").read_text())

# 7. Train until the plan is done or the session clock runs out.
left_min = SESSION_HOURS * 60 - (time.time() - T0) / 60
args = ["--preset", plan["preset"], "--shards", str(SHARDS), "--out", str(WORK),
        "--micro-batch", str(MB), "--accum", str(ACCUM), "--max-steps", str(plan["steps"]),
        "--lr", "6e-4" if plan["preset"] == "base" else "1e-3", "--warmup", "500",
        "--eval-every", "500", "--eval-iters", "40", "--sample-every", "2000",
        "--ckpt-every-min", "30", "--max-minutes", str(max(left_min, 5))]
if major >= 7:  # torch.compile (Triton) needs sm70 or newer
    args.append("--compile")
if (WORK / "latest.pt").exists():
    args += ["--resume", str(WORK / "latest.pt")]
print("train args:", args, flush=True)
status(state="training", gpu=gpu, plan=plan)
rc = subprocess.run([sys.executable, "-m", "noirwrit.train.train", *args]).returncode

log = [json.loads(line) for line in (WORK / "train_log.jsonl").read_text().splitlines() if line.strip()]
done = [r for r in log if r.get("event") == "done"]
evals = [r for r in log if r.get("event") == "eval"]
last_step = max((r.get("step", 0) for r in log), default=0)
finished = bool(done) and done[-1]["reason"] != "time_limit"

if finished:
    src = WORK / ("best.pt" if (WORK / "best.pt").exists() else "latest.pt")
    ck = torch.load(src, map_location="cpu", weights_only=False)
    torch.save({"model": {k: v.half() for k, v in ck["model"].items()}, "config": ck["config"], "step": ck["step"],
                "best_val": ck.get("best_val"), "source": src.name}, WORK / "final-weights.pt")
    (WORK / "DONE.json").write_text(json.dumps({**done[-1], "gpu": gpu, "plan": plan, "weights_from": src.name}, indent=2))
status(state="done" if finished else "session_ended", rc=rc, gpu=gpu, step=last_step, total_steps=plan["steps"],
       last_eval=evals[-1] if evals else None, minutes=round((time.time() - T0) / 60, 1))
shutil.rmtree(SRC, ignore_errors=True)
