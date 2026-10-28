"""Runs inside a Kaggle GPU session. Pushed by tools/online/kaggle_train.py; do not run locally.

Inputs (read-only):
  /kaggle/input/noirwrit-data/      code (noirwrit/), shards/, plan.json (optional)
  /kaggle/input/noirwrit-train-*/   the previous session's output, for resume
Outputs (/kaggle/working, downloaded by the launcher):
  latest.pt, best.pt, train_log.jsonl, plan.txt, plan.json, DONE.json when training finished
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

T0 = time.time()
SESSION_HOURS = 11.3  # Kaggle stops GPU sessions at 12 h; leave room to save
WORK = Path("/kaggle/working")
INPUT = Path("/kaggle/input")

data = next((p for p in INPUT.iterdir() if (p / "shards" / "meta.json").exists()), None)
if data is None:
    sys.exit("noirwrit-data dataset not attached")
# Copy code to a writable place so Python can write bytecode.
SRC = WORK / "src"
if not SRC.exists():
    shutil.copytree(data / "noirwrit", SRC / "noirwrit")
sys.path.insert(0, str(SRC))
os.environ["PYTHONPATH"] = str(SRC)
SHARDS = data / "shards"

# Hugging Face Hub checkpoint push, if the user added an HF_TOKEN secret in the notebook settings.
try:
    from kaggle_secrets import UserSecretsClient

    sec = UserSecretsClient()
    os.environ["HF_TOKEN"] = sec.get_secret("HF_TOKEN")
    os.environ["HF_REPO"] = sec.get_secret("HF_REPO")
except Exception:
    pass

# Resume from the newest checkpoint carried in from the previous session.
prev = sorted((p for p in INPUT.glob("*/latest.pt")), key=lambda p: p.stat().st_mtime)
resume = prev[-1] if prev else None
prev_plan = next(iter(INPUT.glob("*/plan.json")), None) or (data / "plan.json" if (data / "plan.json").exists() else None)
if resume:
    for name in ("train_log.jsonl", "plan.json", "plan.txt"):
        src = resume.parent / name
        if src.exists() and not (WORK / name).exists():
            shutil.copy(src, WORK / name)
    shutil.copy(resume, WORK / "latest.pt")
    if (resume.parent / "best.pt").exists():
        shutil.copy(resume.parent / "best.pt", WORK / "best.pt")

import torch  # noqa: E402

gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "none"
print("GPU:", gpu, flush=True)
if not torch.cuda.is_available():
    sys.exit("no GPU in this session; enable a GPU accelerator")
key = "t4" if "T4" in gpu else "p100" if "P100" in gpu else "a100" if "A100" in gpu else "l4" if "L4" in gpu else "t4"

MB, ACCUM = 16, 2  # 65k tokens per step: enough optimizer steps for a corpus this size
if prev_plan and prev_plan.exists():
    plan = json.loads(prev_plan.read_text())
    if not (WORK / "plan.json").exists():
        shutil.copy(prev_plan, WORK / "plan.json")
else:
    r = subprocess.run([sys.executable, "-m", "noirwrit.train.plan_run", "--gpu", key, "--shards", str(SHARDS),
                        "--budget-usd", "0", "--max-hours", "22", "--micro-batch", str(MB), "--accum", str(ACCUM),
                        "--probe", "--json", str(WORK / "plan.json")], capture_output=True, text=True)
    print(r.stdout, r.stderr[-3000:], flush=True)
    (WORK / "plan.txt").write_text(r.stdout)
    plan = json.loads((WORK / "plan.json").read_text())

left_min = SESSION_HOURS * 60 - (time.time() - T0) / 60
args = ["--preset", plan["preset"], "--shards", str(SHARDS), "--out", str(WORK),
        "--micro-batch", str(MB), "--accum", str(ACCUM), "--max-steps", str(plan["steps"]),
        "--lr", "6e-4" if plan["preset"] == "base" else "1e-3", "--warmup", "500",
        "--eval-every", "500", "--eval-iters", "40", "--sample-every", "2000",
        "--ckpt-every-min", "30", "--max-minutes", str(max(left_min, 5)), "--compile"]
if (WORK / "latest.pt").exists():
    args += ["--resume", str(WORK / "latest.pt")]
print("train args:", args, flush=True)
rc = subprocess.run([sys.executable, "-m", "noirwrit.train.train", *args]).returncode

log = [json.loads(line) for line in (WORK / "train_log.jsonl").read_text().splitlines() if line.strip()]
done = [r for r in log if r.get("event") == "done"]
if done and done[-1]["reason"] != "time_limit":
    (WORK / "DONE.json").write_text(json.dumps({**done[-1], "gpu": gpu, "plan": plan}, indent=2))
shutil.rmtree(SRC, ignore_errors=True)
print("exit", rc, "done" if (WORK / "DONE.json").exists() else "needs another session", flush=True)
