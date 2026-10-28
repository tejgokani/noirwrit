#!/usr/bin/env python3
"""Benchmark generation speed and memory on this Mac. Writes docs/BENCH.md and docs/bench.json.

Speed does not depend on what the weights learned, so the small and base
presets are benchmarked with random weights in the trained model's exact
layout. The trained tiny checkpoint is benchmarked as is.

Usage:
    python tools/guard.py --timeout-min 10 -- python tools/bench.py [--tiny artifacts/tiny/latest.pt]
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch  # noqa: E402

from noirwrit.model.gpt import GPT, PRESETS  # noqa: E402
from noirwrit.runtime.engine import Engine, SampleParams  # noqa: E402
from noirwrit.runtime.export import export_gguf, quantize_gguf  # noqa: E402

WORK = ROOT / "artifacts" / "bench"


def mac_info() -> str:
    chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    mem = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout.strip() or 0) / 1024**3
    return f"{chip or platform.processor()}, {mem:.0f} GB, macOS {platform.mac_ver()[0]}"


def make_ckpt(preset: str) -> Path:
    path = WORK / f"{preset}-random.pt"
    if not path.exists():
        torch.manual_seed(0)
        m = GPT(PRESETS[preset])
        WORK.mkdir(parents=True, exist_ok=True)
        torch.save({"model": m.state_dict(), "config": m.cfg.to_dict(), "step": 0}, path)
    return path


def llama_bench(gguf: Path, n_gen: int = 128, n_prompt: int = 512) -> dict:
    exe = shutil.which("llama-bench")
    r = subprocess.run([exe, "-m", str(gguf), "-p", str(n_prompt), "-n", str(n_gen), "-r", "3", "-o", "json"],
                       capture_output=True, text=True, errors="replace", timeout=900)
    rows = json.loads(r.stdout)
    out = {}
    for row in rows:
        key = "prompt_tok_s" if row.get("n_prompt", 0) > 0 and row.get("n_gen", 0) == 0 else "gen_tok_s"
        out[key] = round(row["avg_ts"], 1)
        out["backend"] = row.get("backends") or row.get("backend")
    return out


def llama_peak_rss(gguf: Path, n: int = 256) -> float:
    """Max RSS in GB of a real llama-completion run (macOS /usr/bin/time -l reports bytes)."""
    exe = shutil.which("llama-completion") or shutil.which("llama-cli")
    r = subprocess.run(["/usr/bin/time", "-l", exe, "-m", str(gguf), "-p", "The fog came in over the harbor and",
                        "-n", str(n), "-c", "2048", "--no-display-prompt", "-no-cnv"],
                       capture_output=True, text=True, errors="replace", timeout=900)
    m = re.search(r"(\d+)\s+maximum resident set size", r.stderr)
    fp = re.search(r"(\d+)\s+peak memory footprint", r.stderr)
    vals = [int(x.group(1)) for x in (m, fp) if x]
    return round(max(vals) / 1024**3, 3) if vals else -1.0


def torch_bench(ckpt: Path, int8: bool, n: int = 128) -> dict:
    eng = Engine.from_checkpoint(ckpt, device="cpu", int8=int8)
    prompt = list(range(10, 266))  # 256-token prompt
    eng.generate(prompt, SampleParams(max_new_tokens=8, seed=1))  # warm up
    eng.generate(prompt, SampleParams(max_new_tokens=n, seed=1))
    return {"gen_tok_s": eng.last_stats["tok_per_s"], "prefill_s": eng.last_stats["prefill_s"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiny", default=str(ROOT / "artifacts" / "tiny" / "latest.pt"))
    ap.add_argument("--presets", default="small,base")
    ap.add_argument("--skip-torch", action="store_true")
    a = ap.parse_args()

    targets = []
    if Path(a.tiny).exists():
        targets.append(("tiny (trained)", Path(a.tiny)))
    for p in a.presets.split(","):
        if p:
            targets.append((f"{p} (random weights)", make_ckpt(p)))

    results = []
    torch.set_num_threads(4)
    for label, ck in targets:
        state = torch.load(ck, map_location="cpu", weights_only=False)
        params = GPT(__import__("noirwrit.model.gpt", fromlist=["GPTConfig"]).GPTConfig(**state["config"])).num_params()
        stem = WORK / (label.split()[0])
        f32 = export_gguf(ck, stem.with_name(stem.name + "-f32.gguf"), name=f"noirwrit-{label.split()[0]}")
        for quant in ("Q8_0", "Q4_K_M"):
            try:
                q = quantize_gguf(f32, quant)
            except subprocess.CalledProcessError:
                continue
            t0 = time.time()
            row = {"model": label, "params_m": round(params / 1e6, 1), "runtime": f"llama.cpp {quant}",
                   "file_mb": round(q.stat().st_size / 1e6, 1), **llama_bench(q), "peak_ram_gb": llama_peak_rss(q)}
            row["seconds"] = round(time.time() - t0, 1)
            results.append(row)
            print(json.dumps(row), flush=True)
        if not a.skip_torch:
            for int8 in (True, False):
                row = {"model": label, "params_m": round(params / 1e6, 1), "runtime": f"PyTorch CPU {'int8' if int8 else 'fp32'}",
                       **torch_bench(ck, int8)}
                results.append(row)
                print(json.dumps(row), flush=True)
        f32.unlink(missing_ok=True)

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    meta = {"machine": mac_info(), "date": time.strftime("%Y-%m-%d"), "llama_cpp": subprocess.run(
        ["llama-cli", "--version"], capture_output=True, text=True).stderr.strip().splitlines()[0] if shutil.which("llama-cli") else ""}
    (docs / "bench.json").write_text(json.dumps({"meta": meta, "results": results}, indent=2))

    lines = [
        "# Benchmarks",
        "",
        f"Machine: {meta['machine']}. Date: {meta['date']}. {meta['llama_cpp']}.",
        "",
        "Generation speed feeds the ETA shown in the app (the worker keeps a rolling average of real tok/s).",
        "Small and base rows use random weights in the exact trained layout; speed and memory do not depend on what the weights learned.",
        "",
        "| Model | Params | Runtime | File | Gen tok/s | Prompt tok/s | Peak RAM |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['model']} | {r['params_m']}M | {r['runtime']} | {str(r.get('file_mb', '')) + ' MB' if r.get('file_mb') else ''} "
                     f"| {r.get('gen_tok_s', '')} | {r.get('prompt_tok_s', '')} | {str(r.get('peak_ram_gb', '')) + ' GB' if r.get('peak_ram_gb') else ''} |")
    base = [r for r in results if r["model"].startswith("base") and r["runtime"] == "llama.cpp Q8_0"]
    if base:
        b = base[0]
        chapter_tokens = 3000 * 1.35
        lines += [
            "",
            "## Quality gates (plan.md section 6) for the base model",
            "",
            f"- Speed, at least 20 tok/s int8: **{b['gen_tok_s']} tok/s** with llama.cpp Q8_0 ({'pass' if b['gen_tok_s'] >= 20 else 'FAIL'}).",
            f"- Laptop RAM under 3 GB during generation: **{b['peak_ram_gb']} GB** peak for llama.cpp ({'pass' if 0 < b['peak_ram_gb'] < 3 else 'check'}).",
            f"- Chapter under 5 min for 3000 words (~{int(chapter_tokens)} tokens): **{chapter_tokens / b['gen_tok_s'] / 60:.1f} min** of pure generation "
            f"({'pass' if chapter_tokens / b['gen_tok_s'] < 300 else 'FAIL'}). Prompt prefill per scene adds a few seconds.",
        ]
    (docs / "BENCH.md").write_text("\n".join(lines) + "\n")
    print((docs / "BENCH.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
