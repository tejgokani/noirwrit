"""Find and load the local model the app should use.

Search order: the model named in settings, then ~/.noirwrit/models, then the
repo's artifacts/ folder. Prefers GGUF through llama.cpp (fast, Metal), then a
PyTorch checkpoint (int8 on CPU). Falls back to the echo generator so the app
still runs (clearly labelled) before any model is trained or downloaded.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from noirwrit.config import HOME, ROOT
from noirwrit.memory.db import DB
from noirwrit.planner.generators import EchoGenerator, Generator, LlamaCppGenerator, TorchGenerator

SEARCH_DIRS = [HOME / "models", ROOT / "artifacts"]


def _skip(p: Path) -> bool:
    """Benchmark files have random weights, and f32 GGUFs are export intermediates."""
    parts = {x.lower() for x in p.parts}
    return bool(parts & {"bench", "probe", "kaggle", "runpod"}) or "random" in p.name or p.stem.endswith("-f32")


def list_models() -> list[dict]:
    out = []
    for d in SEARCH_DIRS:
        if not d.exists():
            continue
        for p in sorted(d.rglob("*.gguf")):
            if _skip(p):
                continue
            out.append({"path": str(p), "kind": "gguf", "name": p.stem, "size_mb": round(p.stat().st_size / 1e6, 1)})
        for p in sorted(d.rglob("*.pt")):
            if _skip(p):
                continue
            if p.name in ("latest.pt", "best.pt") or p.name.endswith("-int8.pt"):
                if p.name.endswith("-int8.pt"):
                    continue  # loaded through the float checkpoint and quantized on the fly
                out.append({"path": str(p), "kind": "torch", "name": f"{p.parent.name}/{p.stem}",
                            "size_mb": round(p.stat().st_size / 1e6, 1)})
    return out


def _rank(m: dict) -> tuple:
    name = m["name"].lower()
    size = 2 if "base" in name else 1 if "small" in name else 0
    has_llama = bool(shutil.which("llama-completion") or shutil.which("llama-cli"))
    gguf_ok = m["kind"] == "gguf" and has_llama
    # Bigger model first, then GGUF (fast, Metal), then Q8 over Q4, then the trained best over latest.
    return (size, gguf_ok, "q8" in name, "best" in name)


def pick_model(db: DB | None = None) -> dict | None:
    """The model the worker will load: the one chosen in Settings, else the best ranked."""
    chosen = db.get_setting("model_path") if db else None
    models = list_models()
    if chosen and Path(chosen).exists():
        return next((m for m in models if m["path"] == chosen),
                    {"path": chosen, "kind": "gguf" if chosen.endswith(".gguf") else "torch", "name": Path(chosen).stem})
    return max(models, key=_rank) if models else None


def load_generator(db: DB | None = None, quality: str = "balanced") -> Generator:
    # Test hook: NOIRWRIT_GENERATOR=echo:<tok_per_s> runs the deterministic stand-in at that speed.
    forced = os.environ.get("NOIRWRIT_GENERATOR", "")
    if forced.startswith("echo"):
        rate = float(forced.split(":", 1)[1]) if ":" in forced else 5000.0
        return EchoGenerator(tok_per_s=rate, simulate_speed=":" in forced)
    pick = pick_model(db)
    if pick is None:
        return EchoGenerator()
    # Lower temperature reads more grammatical; best-of-N reranking adds the variety back.
    temp = {"fast": 0.7, "balanced": 0.75, "quality": 0.8}.get(quality, 0.75)
    try:
        if pick["kind"] == "gguf":
            return LlamaCppGenerator(pick["path"], temperature=temp)
        return TorchGenerator(pick["path"], device="cpu", int8=True, temperature=temp)
    except Exception:
        return EchoGenerator()


HF_REPO = "tejgokani/noirwrit-base"  # where release weights are published
HF_FILE = "noirwrit-base-q8_0.gguf"


def install_model(source: str = "") -> str:
    """Copy or download a GGUF into ~/.noirwrit/models. Setup step; the app itself never downloads."""
    dest_dir = HOME / "models"
    dest_dir.mkdir(parents=True, exist_ok=True)
    local = Path(source).expanduser() if source else ROOT / "artifacts" / "base" / "export" / HF_FILE
    if local.suffix == ".gguf" and local.exists():
        dest = dest_dir / local.name
        if dest.resolve() != local.resolve():
            shutil.copy(local, dest)
        return f"installed {dest}"
    repo = source if source and "/" in source and not source.endswith(".gguf") else HF_REPO
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        return "huggingface_hub is not installed: pip install huggingface_hub, or pass a local .gguf path"
    path = hf_hub_download(repo, HF_FILE, local_dir=str(dest_dir))
    return f"installed {path} from {repo}"
