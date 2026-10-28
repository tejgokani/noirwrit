#!/usr/bin/env python3
"""Fallback: train on a rented RunPod RTX 4090 with a hard dollar cap. Only if Kaggle cannot finish.

Needs RUNPOD_API_KEY, HF_TOKEN and HF_REPO in .env (see docs/ONLINE_TRAINING.md).
    python tools/online/runpod_train.py --budget-usd 8

Flow: upload the bundle (code, tokenizer, shards) to a private Hugging Face dataset repo,
start one pod, the pod downloads the bundle, plans the run against the budget with a
2-minute probe, trains with checkpoints pushed to the Hub every 30 minutes, then stops
itself. This launcher also polls the pod and deletes it if the bill reaches the cap.

Status: written against the RunPod REST API (rest.runpod.io/v1) but not yet run, since it
needs a paid account. Never debug on a paid GPU: prove changes on the Mac tiny run first.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = "https://rest.runpod.io/v1"
GPU = "NVIDIA GeForce RTX 4090"
IMAGE = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"

POD_SCRIPT = r"""
set -e
pip install -q "tokenizers>=0.19" "huggingface_hub>=0.23" numpy psutil
python - <<'PY'
from huggingface_hub import hf_hub_download
import tarfile, os
p = hf_hub_download(os.environ["HF_REPO"], "bundle.tar.gz", repo_type="dataset", token=os.environ["HF_TOKEN"])
tarfile.open(p).extractall("/workspace/nw")
PY
cd /workspace/nw
python -m noirwrit.train.plan_run --gpu rtx4090 --shards shards --cost-per-hour "$COST_PER_HOUR" \
  --budget-usd "$BUDGET_USD" --max-hours 24 --micro-batch 32 --accum 1 --probe --json plan.json | tee plan.txt
PRESET=$(python -c "import json;print(json.load(open('plan.json'))['preset'])")
STEPS=$(python -c "import json;print(json.load(open('plan.json'))['steps'])")
python -m noirwrit.train.train --preset "$PRESET" --shards shards --out /workspace/out \
  --micro-batch 32 --accum 1 --max-steps "$STEPS" --lr 6e-4 --warmup 500 --eval-every 500 \
  --ckpt-every-min 30 --compile --cost-per-hour "$COST_PER_HOUR" --budget-usd "$BUDGET_USD" || true
python - <<'PY'
from huggingface_hub import HfApi
import os
api = HfApi(token=os.environ["HF_TOKEN"])
for f in ("latest.pt", "best.pt", "train_log.jsonl"):
    p = f"/workspace/out/{f}"
    if os.path.exists(p):
        api.upload_file(path_or_fileobj=p, path_in_repo=f"final/{f}", repo_id=os.environ["HF_REPO"], repo_type="model")
api.upload_file(path_or_fileobj="plan.txt", path_in_repo="final/plan.txt", repo_id=os.environ["HF_REPO"], repo_type="model")
PY
runpodctl stop pod "$RUNPOD_POD_ID"
"""


def load_env() -> dict:
    env = dict(os.environ)
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"'))
    for k in ("RUNPOD_API_KEY", "HF_TOKEN", "HF_REPO"):
        if not env.get(k):
            sys.exit(f"missing {k} in .env; see docs/ONLINE_TRAINING.md")
    return env


def call(method: str, path: str, key: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    return json.loads(raw) if raw else {}


def upload_bundle(env: dict) -> None:
    from huggingface_hub import HfApi

    tmp = ROOT / "artifacts" / "runpod"
    tmp.mkdir(parents=True, exist_ok=True)
    tar = tmp / "bundle.tar.gz"
    with tarfile.open(tar, "w:gz") as t:
        t.add(ROOT / "noirwrit", "noirwrit", filter=lambda i: None if "__pycache__" in i.name or "/static" in i.name else i)
        t.add(ROOT / "data" / "shards", "shards")
    api = HfApi(token=env["HF_TOKEN"])
    api.create_repo(env["HF_REPO"], repo_type="dataset", private=True, exist_ok=True)
    api.create_repo(env["HF_REPO"], repo_type="model", private=True, exist_ok=True)
    api.upload_file(path_or_fileobj=str(tar), path_in_repo="bundle.tar.gz", repo_id=env["HF_REPO"], repo_type="dataset")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-usd", type=float, default=8.0)
    ap.add_argument("--max-bid", type=float, default=0.6, help="refuse pods above this $/hr")
    a = ap.parse_args()
    env = load_env()
    key = env["RUNPOD_API_KEY"]
    print("uploading bundle to the Hub (private)...", flush=True)
    upload_bundle(env)
    pod = call("POST", "/pods", key, {
        "name": "noirwrit-train", "imageName": IMAGE, "gpuTypeIds": [GPU], "gpuCount": 1,
        "cloudType": "COMMUNITY", "containerDiskInGb": 30, "volumeInGb": 0,
        "env": {"HF_TOKEN": env["HF_TOKEN"], "HF_REPO": env["HF_REPO"], "BUDGET_USD": str(a.budget_usd),
                "COST_PER_HOUR": str(a.max_bid)},
        "dockerStartCmd": ["bash", "-lc", POD_SCRIPT],
    })
    pid = pod["id"]
    rate = float(pod.get("costPerHr") or a.max_bid)
    if rate > a.max_bid:
        call("DELETE", f"/pods/{pid}", key)
        sys.exit(f"pod rate ${rate}/hr is above --max-bid ${a.max_bid}; deleted")
    print(f"pod {pid} at ${rate}/hr; hard cap ${a.budget_usd}", flush=True)
    t0 = time.time()
    try:
        while True:
            time.sleep(120)
            info = call("GET", f"/pods/{pid}", key)
            spent = (time.time() - t0) / 3600 * rate
            status = info.get("desiredStatus")
            print(f"{time.strftime('%H:%M')} status={status} spent=${spent:.2f}", flush=True)
            if status in ("EXITED", "TERMINATED") or spent >= a.budget_usd:
                break
    finally:
        # Never leave a paid pod running.
        try:
            call("DELETE", f"/pods/{pid}", key)
            print("pod deleted", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"could not delete pod {pid}: {e}. Delete it at runpod.io/console now.", flush=True)
    print(f"checkpoints are in the Hub repo {env['HF_REPO']} under final/", flush=True)
    shutil.rmtree(ROOT / "artifacts" / "runpod", ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
