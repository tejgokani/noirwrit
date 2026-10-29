"""Plan an online training run: FLOPs math, a 2-minute speed probe, and the budget rule.

plan.md section 5: log FLOPs ~ 6 x params x tokens before launch, compare with
measured throughput, print hours and dollars, and drop to the small model (or
fewer tokens) automatically when the projection exceeds the budget.

Usage:
    python -m noirwrit.train.plan_run --gpu t4 --budget-usd 0 --max-hours 11
    python -m noirwrit.train.plan_run --gpu rtx4090 --cost-per-hour 0.45 --budget-usd 8 --probe
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from noirwrit.model.gpt import GPT, PRESETS

# Dense half-precision peak TFLOPs and a realistic model FLOPs utilization for a ~100M GPT.
GPUS = {
    "t4": {"peak_tflops": 65.0, "mfu": 0.22, "usd_per_hour": 0.0},
    "p100": {"peak_tflops": 18.7, "mfu": 0.35, "usd_per_hour": 0.0},
    "a100": {"peak_tflops": 312.0, "mfu": 0.35, "usd_per_hour": 1.2},
    "rtx4090": {"peak_tflops": 165.0, "mfu": 0.35, "usd_per_hour": 0.45},
    "l4": {"peak_tflops": 121.0, "mfu": 0.3, "usd_per_hour": 0.0},
}

MAX_EPOCHS = 4.0


@dataclass
class Plan:
    preset: str
    params: int
    tokens: int
    steps: int
    tokens_per_step: int
    flops: float
    tok_per_s: float
    hours: float
    usd: float
    source: str  # estimate | probe
    note: str = ""
    micro_batch: int = 0
    accum: int = 0


def params_of(preset: str) -> int:
    return GPT(PRESETS[preset]).num_params()


def corpus_tokens(shards: Path) -> int:
    meta = json.loads((shards / "meta.json").read_text())
    return sum(c["train"] for c in meta["counts"].values())


def tok_per_s_estimate(params: int, gpu: str) -> float:
    g = GPUS[gpu]
    return g["peak_tflops"] * 1e12 * g["mfu"] / (6 * params)


def make_plan(preset: str, train_tokens: int, tok_s: float, usd_hr: float, tokens_per_step: int, source: str) -> Plan:
    p = params_of(preset)
    tokens = int(train_tokens)
    steps = max(1, tokens // tokens_per_step)
    tokens = steps * tokens_per_step
    hours = tokens / tok_s / 3600
    return Plan(preset, p, tokens, steps, tokens_per_step, 6.0 * p * tokens, round(tok_s), round(hours, 2),
                round(hours * usd_hr, 2), source)


def choose(corpus: int, tok_s_by_preset: dict[str, float], usd_hr: float, budget_usd: float, max_hours: float,
           tokens_per_step: int, source: str) -> Plan:
    """Largest preset and most tokens (up to MAX_EPOCHS) that fit both the time cap and the budget."""
    want = int(corpus * MAX_EPOCHS)
    for preset in ("base", "small"):
        if preset not in tok_s_by_preset:
            continue
        tok_s = tok_s_by_preset[preset]
        cap_hours = max_hours
        if usd_hr > 0 and budget_usd > 0:
            cap_hours = min(cap_hours, budget_usd * 0.9 / usd_hr)  # 10% margin under the hard cap
        fit_tokens = int(tok_s * cap_hours * 3600)
        tokens = min(want, fit_tokens)
        # Under one epoch, the smaller model learns more from the same compute.
        if preset == "base" and tokens < corpus:
            continue
        plan = make_plan(preset, tokens, tok_s, usd_hr, tokens_per_step, source)
        if tokens < want:
            plan.note = f"cut to {tokens / corpus:.1f} epochs to fit {cap_hours:.1f} h"
        return plan
    small = make_plan("small", min(want, int(tok_s_by_preset.get("small", 1) * max_hours * 3600)),
                      tok_s_by_preset.get("small", 1), usd_hr, tokens_per_step, source)
    small.note = "base does not fit one epoch in the cap; small chosen"
    return small


def probe(preset: str, shards: Path, micro_batch: int, accum: int, minutes: float = 2.0) -> tuple[float, int, int]:
    """Train for a couple of minutes; return (median tok/s after warmup, micro_batch, accum).

    On out-of-memory it halves the micro-batch and doubles accumulation, so the
    tokens per optimizer step stay the same. Other failures raise with the
    subprocess's own error message.
    """
    mb, acc = micro_batch, accum
    while mb >= 1:
        with tempfile.TemporaryDirectory() as tmp:
            cmd = [sys.executable, "-m", "noirwrit.train.train", "--preset", preset, "--shards", str(shards),
                   "--out", tmp, "--micro-batch", str(mb), "--accum", str(acc), "--max-steps", "100000",
                   "--max-minutes", str(minutes), "--eval-every", "100000", "--sample-every", "0",
                   "--ckpt-every-min", "1000"]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0:
                rates = [json.loads(line)["tok_per_s"] for line in (Path(tmp) / "train_log.jsonl").read_text().splitlines()
                         if '"tok_per_s"' in line]
                rates = sorted(rates[len(rates) // 3:]) or [1.0]  # drop warmup
                return float(rates[len(rates) // 2]), mb, acc
        err = (r.stderr or r.stdout)[-3000:]
        if "out of memory" in err.lower() and mb > 1:
            print(f"{preset}: out of memory at micro-batch {mb}; retrying at {mb // 2}", file=sys.stderr, flush=True)
            mb, acc = mb // 2, acc * 2
            continue
        raise RuntimeError(f"probe for {preset} failed (micro-batch {mb}):\n{err}")
    raise RuntimeError(f"probe for {preset}: out of memory even at micro-batch 1")


def report(plan: Plan, corpus: int, gpu: str, budget: float) -> str:
    lines = [
        f"Corpus: {corpus:,} train tokens. GPU: {gpu}. Budget: ${budget:.2f}.",
        f"Model: {plan.preset} ({plan.params / 1e6:.1f}M params). Tokens: {plan.tokens:,} ({plan.tokens / corpus:.2f} epochs).",
        f"FLOPs ~ 6 x {plan.params:.3g} x {plan.tokens:.3g} = {plan.flops:.3g}",
        f"Throughput ({plan.source}): {plan.tok_per_s:,} tok/s. Estimated time: {plan.hours:.2f} h. Estimated cost: ${plan.usd:.2f}.",
        f"Steps: {plan.steps:,} of {plan.tokens_per_step:,} tokens.",
    ]
    if plan.note:
        lines.append(f"Note: {plan.note}.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", default="t4", choices=list(GPUS))
    ap.add_argument("--shards", default="data/shards")
    ap.add_argument("--cost-per-hour", type=float, default=None)
    ap.add_argument("--budget-usd", type=float, default=8.0)
    ap.add_argument("--max-hours", type=float, default=11.0, help="Kaggle sessions stop at 12 h")
    ap.add_argument("--micro-batch", type=int, default=16)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--ctx", type=int, default=2048)
    ap.add_argument("--probe", action="store_true", help="measure real tok/s for 2 minutes per preset")
    ap.add_argument("--json", default="", help="write the chosen plan here")
    a = ap.parse_args(argv)

    shards = Path(a.shards)
    corpus = corpus_tokens(shards)
    usd_hr = GPUS[a.gpu]["usd_per_hour"] if a.cost_per_hour is None else a.cost_per_hour
    tps_step = a.micro_batch * a.accum * a.ctx
    batch = {p: (a.micro_batch, a.accum) for p in ("base", "small")}
    if a.probe:
        rates = {}
        for p in ("base", "small"):
            rate, mb, acc = probe(p, shards, a.micro_batch, a.accum)
            rates[p], batch[p] = rate, (mb, acc)
        source = "probe"
    else:
        rates = {p: tok_per_s_estimate(params_of(p), a.gpu) for p in ("base", "small")}
        source = "estimate"
    plan = choose(corpus, rates, usd_hr, a.budget_usd, a.max_hours, tps_step, source)
    plan.micro_batch, plan.accum = batch[plan.preset]
    print(report(plan, corpus, a.gpu, a.budget_usd))
    if a.json:
        Path(a.json).write_text(json.dumps(asdict(plan), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
