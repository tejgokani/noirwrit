"""Paths and the Phase 0 requirements file."""

from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
HOME = Path(os.environ.get("NOIRWRIT_HOME", Path.home() / ".noirwrit"))

_DEFAULT_REQUIREMENTS = {
    "interface": "web",
    "dependency_policy": "own_model_plus_tiny_embedder",
    "embedder": "sentence-transformers/all-MiniLM-L6-v2",
    "max_budget_usd": 8,
    "generation_defaults": {
        "chapter_words": 3000,
        "genre_mix": {"noir": 0.5, "classic_detective": 0.3, "thriller": 0.2},
        "language": "en",
    },
}


def load_requirements() -> dict:
    """Read config/requirements.json from a source checkout, else use defaults."""
    path = ROOT / "config" / "requirements.json"
    if path.exists():
        return json.loads(path.read_text())
    return dict(_DEFAULT_REQUIREMENTS)
