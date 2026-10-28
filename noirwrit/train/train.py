"""Train a Noirwrit GPT on the packed shards.

Three-stage curriculum (plan.md section 5, rule 8): general fiction (short),
crime/detective (long), then the noir voice set (short, lower learning rate,
early stop if val loss rises).

Usage (local smoke test, always through the guard on a Mac):
    python tools/guard.py --timeout-min 10 -- \\
        python -m noirwrit.train.train --preset tiny --max-minutes 8 --out artifacts/tiny

Resume:
    python -m noirwrit.train.train --resume artifacts/tiny/latest.pt ...
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from noirwrit.config import ROOT
from noirwrit.model.gpt import GPT, PRESETS, GPTConfig

SHARDS = ROOT / "data" / "shards"


@dataclass
class Stage:
    name: str  # shard set: general | crime | noir
    share: float  # share of total steps
    lr_scale: float
    early_stop: bool = False


DEFAULT_STAGES = [
    Stage("general", 0.15, 1.0),
    Stage("crime", 0.75, 1.0),
    Stage("noir", 0.10, 0.3, early_stop=True),
]


def parse_stages(spec: str) -> list[Stage]:
    """Format: name:share:lr_scale[:es], comma separated. e.g. general:0.15:1,crime:0.75:1,noir:0.1:0.3:es"""
    out = []
    for part in spec.split(","):
        bits = part.split(":")
        out.append(Stage(bits[0], float(bits[1]), float(bits[2]) if len(bits) > 2 else 1.0, len(bits) > 3 and bits[3] == "es"))
    total = sum(s.share for s in out)
    for s in out:
        s.share /= total
    return out


class ShardLoader:
    def __init__(self, shard_dir: Path, name: str, ctx: int, device: str, seed: int = 0):
        self.ctx = ctx
        self.device = device
        self.train = self._open(shard_dir / f"{name}_train.bin")
        self.val = self._open(shard_dir / f"{name}_val.bin")
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def _open(path: Path) -> np.ndarray:
        if not path.exists() or path.stat().st_size == 0:
            raise FileNotFoundError(f"missing shard {path}")
        return np.memmap(path, dtype=np.uint16, mode="r")

    def batch(self, bsz: int, split: str = "train") -> tuple[torch.Tensor, torch.Tensor]:
        data = self.train if split == "train" else self.val
        hi = len(data) - self.ctx - 1
        if hi <= 0:
            raise ValueError(f"shard too small for ctx {self.ctx}")
        ix = self.rng.integers(0, hi, size=bsz)
        x = np.stack([data[i:i + self.ctx].astype(np.int64) for i in ix])
        y = np.stack([data[i + 1:i + 1 + self.ctx].astype(np.int64) for i in ix])
        xt, yt = torch.from_numpy(x), torch.from_numpy(y)
        if self.device == "cuda":
            return xt.pin_memory().to(self.device, non_blocking=True), yt.pin_memory().to(self.device, non_blocking=True)
        return xt.to(self.device), yt.to(self.device)


def pick_device(pref: str = "auto") -> str:
    if pref != "auto":
        return pref
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def pick_dtype(device: str, pref: str = "auto") -> torch.dtype:
    if pref == "fp32":
        return torch.float32
    if pref == "bf16":
        return torch.bfloat16
    if pref == "fp16":
        return torch.float16
    if device == "cuda":
        return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return torch.float32  # MPS autocast is still uneven; tiny runs do not need it


def lr_at(step: int, total: int, warmup: int, max_lr: float, min_lr: float) -> float:
    if step < warmup:
        return max_lr * (step + 1) / warmup
    if step >= total:
        return min_lr
    ratio = (step - warmup) / max(total - warmup, 1)
    return min_lr + 0.5 * (1 + math.cos(math.pi * ratio)) * (max_lr - min_lr)


def save_checkpoint(path: Path, model: GPT, opt, step: int, args: dict, extra: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    raw = model._orig_mod if hasattr(model, "_orig_mod") else model
    torch.save({
        "model": raw.state_dict(),
        "optimizer": opt.state_dict(),
        "config": raw.cfg.to_dict(),
        "step": step,
        "args": args,
        **extra,
    }, tmp)
    tmp.replace(path)


@torch.no_grad()
def estimate_loss(model: GPT, loader: ShardLoader, bsz: int, iters: int, ctx) -> float:
    model.eval()
    losses = []
    for _ in range(iters):
        x, y = loader.batch(bsz, "val")
        with ctx:
            _, loss = model(x, y)
        losses.append(loss.item())
    model.train()
    return float(np.mean(losses))


@torch.no_grad()
def sample_text(model: GPT, tok, prompt: str, n: int, device: str, temperature: float = 0.8, top_k: int = 50) -> str:
    raw = model._orig_mod if hasattr(model, "_orig_mod") else model
    raw.eval()
    ids = tok.encode(prompt).ids
    x = torch.tensor([ids], device=device)
    for _ in range(n):
        x_cond = x[:, -raw.cfg.ctx_len:]
        logits, _ = raw(x_cond)
        logits = logits[:, -1, :].float() / temperature
        v, _ = torch.topk(logits, top_k)
        logits[logits < v[:, [-1]]] = -float("inf")
        nxt = torch.multinomial(torch.softmax(logits, -1), 1)
        x = torch.cat([x, nxt], dim=1)
    raw.train()
    return tok.decode(x[0].tolist())


def maybe_push_hub(path: Path, log) -> None:
    """Upload a checkpoint to the Hugging Face Hub if HF_REPO and HF_TOKEN are set."""
    repo = os.environ.get("HF_REPO")
    if not repo or not os.environ.get("HF_TOKEN"):
        return
    try:
        from huggingface_hub import HfApi

        HfApi().upload_file(path_or_fileobj=str(path), path_in_repo=f"checkpoints/{path.name}", repo_id=repo, repo_type="model")
        log({"event": "hub_push", "file": path.name, "repo": repo})
    except Exception as e:  # never kill training over an upload
        log({"event": "hub_push_failed", "error": repr(e)})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default="tiny", choices=list(PRESETS))
    ap.add_argument("--ctx", type=int, default=0, help="override context length")
    ap.add_argument("--shards", default=str(SHARDS))
    ap.add_argument("--stages", default="", help="see parse_stages; default general/crime/noir")
    ap.add_argument("--out", default="artifacts/run")
    ap.add_argument("--resume", default="")
    ap.add_argument("--micro-batch", type=int, default=16)
    ap.add_argument("--accum", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=2000)
    ap.add_argument("--max-minutes", type=float, default=0, help="stop cleanly after N minutes (0 = no limit)")
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--min-lr-ratio", type=float, default=0.1)
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--weight-decay", type=float, default=0.1)
    ap.add_argument("--grad-clip", type=float, default=1.0)
    ap.add_argument("--eval-every", type=int, default=100)
    ap.add_argument("--eval-iters", type=int, default=20)
    ap.add_argument("--sample-every", type=int, default=500)
    ap.add_argument("--ckpt-every-min", type=float, default=30.0)
    ap.add_argument("--device", default="auto")
    ap.add_argument("--dtype", default="auto", choices=["auto", "fp32", "bf16", "fp16"])
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--cost-per-hour", type=float, default=0.0)
    ap.add_argument("--budget-usd", type=float, default=0.0, help="abort when running cost reaches this")
    ap.add_argument("--seed", type=int, default=1337)
    a = ap.parse_args(argv)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log_f = (out / "train_log.jsonl").open("a")

    def log(rec: dict) -> None:
        rec = {"t": round(time.time(), 1), **rec}
        log_f.write(json.dumps(rec) + "\n")
        log_f.flush()
        print(json.dumps(rec), flush=True)

    device = pick_device(a.device)
    dtype = pick_dtype(device, a.dtype)
    torch.manual_seed(a.seed)
    if device == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    state = None
    if a.resume:
        state = torch.load(a.resume, map_location="cpu", weights_only=False)
        cfg = GPTConfig(**state["config"])
    else:
        cfg = GPTConfig(**PRESETS[a.preset].to_dict())
        if a.ctx:
            cfg.ctx_len = a.ctx
    model = GPT(cfg).to(device)
    opt = model.configure_optimizer(a.lr, a.weight_decay, device_type=device)
    start_step = 0
    best_val = float("inf")
    stage_best: dict[str, float] = {}
    if state:
        model.load_state_dict(state["model"])
        opt.load_state_dict(state["optimizer"])
        start_step = state["step"]
        best_val = state.get("best_val", best_val)
        stage_best = state.get("stage_best", {})
        log({"event": "resumed", "from": a.resume, "step": start_step})

    stages = parse_stages(a.stages) if a.stages else DEFAULT_STAGES
    total = a.max_steps
    bounds, acc = [], 0
    for s in stages:
        n = max(1, round(s.share * total))
        bounds.append((acc, acc + n, s))
        acc += n
    total = acc
    loaders = {s.name: ShardLoader(Path(a.shards), s.name, cfg.ctx_len, device, seed=a.seed + i) for i, s in enumerate(stages)}

    tok = None
    try:
        from noirwrit.tokenizer.train_tokenizer import load_tokenizer

        tok = load_tokenizer()
    except Exception:
        pass

    use_scaler = dtype == torch.float16
    scaler = torch.amp.GradScaler("cuda", enabled=use_scaler) if device == "cuda" else None
    amp_ctx = torch.autocast(device_type=device, dtype=dtype) if dtype != torch.float32 else nullcontext()
    train_model = torch.compile(model) if a.compile else model

    tokens_per_step = a.micro_batch * a.accum * cfg.ctx_len
    log({"event": "start", "device": device, "dtype": str(dtype), "params": model.num_params(),
         "config": cfg.to_dict(), "total_steps": total, "tokens_per_step": tokens_per_step,
         "stages": [(lo, hi, s.name, s.lr_scale) for lo, hi, s in bounds]})

    t0 = time.time()
    last_ckpt = time.time()
    tok_count = 0
    rate_t0, rate_tok = time.time(), 0
    noir_bad_evals = 0
    step = start_step
    stop_reason = "max_steps"

    def stage_for(st: int) -> Stage:
        for lo, hi, s in bounds:
            if lo <= st < hi:
                return s
        return bounds[-1][2]

    def checkpoint(tag: str = "latest") -> None:
        p = out / f"{tag}.pt"
        save_checkpoint(p, model, opt, step, vars(a), {"best_val": best_val, "stage_best": stage_best})
        log({"event": "checkpoint", "file": str(p), "step": step})
        maybe_push_hub(p, log)

    model.train()
    while step < total:
        stage = stage_for(step)
        loader = loaders[stage.name]
        lr = lr_at(step, total, a.warmup, a.lr, a.lr * a.min_lr_ratio) * stage.lr_scale
        for g in opt.param_groups:
            g["lr"] = lr

        opt.zero_grad(set_to_none=True)
        loss_acc = 0.0
        for _ in range(a.accum):
            x, y = loader.batch(a.micro_batch)
            with amp_ctx:
                _, loss = train_model(x, y)
                loss = loss / a.accum
            loss_acc += loss.item()
            if scaler:
                scaler.scale(loss).backward()
            else:
                loss.backward()
        if scaler:
            scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), a.grad_clip)
        if scaler:
            scaler.step(opt)
            scaler.update()
        else:
            opt.step()
        step += 1
        tok_count += tokens_per_step
        rate_tok += tokens_per_step

        if step % 10 == 0 or step == 1:
            now = time.time()
            tps = rate_tok / max(now - rate_t0, 1e-6)
            rate_t0, rate_tok = now, 0
            elapsed_h = (now - t0) / 3600
            rec = {"step": step, "stage": stage.name, "loss": round(loss_acc, 4), "lr": round(lr, 6),
                   "grad_norm": round(float(gn), 3), "tok_per_s": round(tps), "elapsed_min": round(elapsed_h * 60, 2)}
            if a.cost_per_hour:
                rec["cost_usd"] = round(elapsed_h * a.cost_per_hour, 3)
                remaining_h = (total - step) * tokens_per_step / max(tps, 1) / 3600
                rec["projected_total_usd"] = round((elapsed_h + remaining_h) * a.cost_per_hour, 2)
            log(rec)
            if a.budget_usd and a.cost_per_hour and elapsed_h * a.cost_per_hour >= a.budget_usd:
                stop_reason = "budget"
                break

        if step % a.eval_every == 0 or step == total:
            vl = estimate_loss(model, loader, a.micro_batch, a.eval_iters, amp_ctx)
            log({"event": "eval", "step": step, "stage": stage.name, "val_loss": round(vl, 4)})
            prev = stage_best.get(stage.name, float("inf"))
            if vl < prev:
                stage_best[stage.name] = vl
                noir_bad_evals = 0
            elif stage.early_stop:
                noir_bad_evals += 1
            if vl < best_val:
                best_val = vl
            # Keep the best checkpoint per final stage only; earlier stages see different data.
            if stage is bounds[-1][2] and vl <= stage_best.get(stage.name, vl):
                checkpoint("best")
            if stage.early_stop and noir_bad_evals >= 2:
                stop_reason = "early_stop_noir_val_rising"
                break

        if tok is not None and a.sample_every and step % a.sample_every == 0:
            s = sample_text(model, tok, "The detective looked at the body and", 80, device)
            log({"event": "sample", "step": step, "text": s})

        if time.time() - last_ckpt > a.ckpt_every_min * 60:
            checkpoint()
            last_ckpt = time.time()

        if a.max_minutes and time.time() - t0 > a.max_minutes * 60:
            stop_reason = "time_limit"
            break

    checkpoint()
    if tok is not None:
        s = sample_text(model, tok, "The detective looked at the body and", 120, device)
        log({"event": "sample", "step": step, "text": s})
    log({"event": "done", "step": step, "reason": stop_reason, "tokens_seen": tok_count,
         "best_val": best_val, "stage_best": stage_best, "minutes": round((time.time() - t0) / 60, 2)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
