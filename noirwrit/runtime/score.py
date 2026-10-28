"""Score candidate continuations so the story engine can keep the best of N.

Two parts:
- Model score: mean log-probability of the candidate under the PyTorch checkpoint
  that matches the GGUF in use (when one is available).
- Text score: cheap checks that catch what reads as broken English: words that
  are not in the dictionary, repeated phrases, unbalanced quotation marks, and
  runaway sentences.
"""

from __future__ import annotations

import math
import re
from functools import lru_cache
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z]+(?:'[a-z]+)?")
DICT_PATHS = ("/usr/share/dict/words", "/usr/dict/words")


@lru_cache(maxsize=1)
def dictionary() -> frozenset[str]:
    words: set[str] = set()
    for p in DICT_PATHS:
        if Path(p).exists():
            words |= {w.strip().lower() for w in Path(p).read_text(errors="ignore").splitlines() if w.strip()}
            break
    try:
        # Words the corpus uses that a plain dictionary may miss.
        from noirwrit.tokenizer.train_tokenizer import TOKENIZER_PATH

        if TOKENIZER_PATH.exists():
            import json

            vocab = json.loads(TOKENIZER_PATH.read_text())["model"]["vocab"]
            words |= {t.lstrip("Ġ").lower() for t in vocab if t.startswith("Ġ") and t[1:].isalpha() and len(t) > 3}
    except Exception:
        pass
    return frozenset(words)


def _known(w: str, d: frozenset[str]) -> bool:
    lw = w.lower()
    if lw in d or (lw.endswith("'s") and lw[:-2] in d):
        return True
    for suf in ("s", "es", "ed", "d", "ing", "ly", "er", "est"):
        if lw.endswith(suf) and lw[: -len(suf)] in d:
            return True
    return w[:1].isupper()  # capitalized words may be names


def text_stats(text: str) -> dict:
    words = WORD_RE.findall(text)
    d = dictionary()
    n = max(len(words), 1)
    nonword = sum(not _known(w, d) for w in words) / n if d else 0.0
    low = [w.lower() for w in words]
    tri = [tuple(low[i:i + 3]) for i in range(len(low) - 2)]
    repeat3 = 1 - len(set(tri)) / len(tri) if tri else 0.0
    quotes_odd = text.count('"') % 2
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    long_sent = sum(len(s.split()) > 45 for s in sentences) / max(len(sentences), 1)
    hyphen_junk = len(re.findall(r"\b\w+-\w+-\w+\b|\w-\w{1,2}\b", text)) / n
    return {"nonword": nonword, "repeat3": repeat3, "quotes_odd": quotes_odd, "long_sent": long_sent,
            "hyphen_junk": hyphen_junk, "words": len(words)}


def text_score(text: str) -> float:
    """Higher is better. Zero is clean text; penalties are roughly in nats per token."""
    st = text_stats(text)
    if st["words"] < 5:
        return -5.0
    return -(6.0 * st["nonword"] + 4.0 * st["repeat3"] + 0.4 * st["quotes_odd"] + 1.0 * st["long_sent"]
             + 3.0 * st["hyphen_junk"])


class ModelScorer:
    """Mean token log-probability of a continuation under a Noirwrit PyTorch checkpoint."""

    def __init__(self, ckpt: str | Path, device: str = "cpu"):
        import torch

        from noirwrit.runtime.engine import load_checkpoint
        from noirwrit.tokenizer.train_tokenizer import load_tokenizer

        self.torch = torch
        self.model = load_checkpoint(ckpt, device)
        self.tok = load_tokenizer()
        self.device = device

    def mean_logprob(self, context: str, continuation: str) -> float:
        torch = self.torch
        ctx = self.tok.encode(context).ids
        cont = self.tok.encode(continuation).ids
        if not cont:
            return -10.0
        max_len = self.model.cfg.ctx_len
        ids = (ctx + cont)[-max_len:]
        n_cont = min(len(cont), len(ids) - 1)
        x = torch.tensor([ids[:-1]], device=self.device)
        y = torch.tensor([ids[1:]], device=self.device)
        with torch.no_grad():
            logits, _ = self.model(x, y)
            lp = torch.log_softmax(logits[0, -n_cont:].float(), -1)
            picked = lp.gather(1, y[0, -n_cont:].unsqueeze(1)).squeeze(1)
        return float(picked.mean())


def find_scorer_ckpt(model_path: str | Path) -> Path | None:
    """The .pt checkpoint next to an exported GGUF (artifacts/<run>/export/x.gguf -> artifacts/<run>/best.pt)."""
    p = Path(model_path)
    if p.suffix == ".pt":
        return p
    for base in (p.parent, p.parent.parent):
        for name in ("best.pt", "latest.pt"):
            if (base / name).exists():
                return base / name
    return None


def combined(model_lp: float | None, text: str) -> float:
    # Model log-prob is about -2 to -5 per token; text penalties sit on a similar scale.
    return (model_lp if model_lp is not None and math.isfinite(model_lp) else 0.0) + text_score(text)
