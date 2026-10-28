"""Sentence embedders.

MiniLMEmbedder: the one tiny pretrained model the dependency policy allows
(all-MiniLM-L6-v2, ~22M params, 384 dims). It is downloaded once during setup
and loaded offline at runtime.

HashingEmbedder: a no-download fallback built from hashed word unigrams and
bigrams. It is deterministic, which also makes it the embedder for tests.
"""

from __future__ import annotations

import hashlib
import os
import re
from functools import lru_cache

import numpy as np

DIM = 384
WORD_RE = re.compile(r"[a-z0-9']+")


class Embedder:
    dim = DIM
    name = "base"

    def embed(self, texts: list[str]) -> np.ndarray:  # (n, dim) float32, L2 normalized
        raise NotImplementedError

    def embed_one(self, text: str) -> np.ndarray:
        return self.embed([text])[0]


class HashingEmbedder(Embedder):
    name = "hashing"

    def __init__(self, dim: int = DIM):
        self.dim = dim

    @staticmethod
    @lru_cache(maxsize=200_000)
    def _h(tok: str) -> tuple[int, float]:
        d = hashlib.blake2b(tok.encode(), digest_size=8).digest()
        v = int.from_bytes(d, "little")
        return v, 1.0 if (v >> 63) & 1 else -1.0

    def embed(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            words = WORD_RE.findall(t.lower())
            feats = words + [a + " " + b for a, b in zip(words, words[1:], strict=False)]
            for f in feats:
                h, sign = self._h(f)
                out[i, h % self.dim] += sign
            # Sublinear term weighting, then L2 normalize.
            out[i] = np.sign(out[i]) * np.log1p(np.abs(out[i]))
            n = np.linalg.norm(out[i])
            if n > 0:
                out[i] /= n
        return out


class MiniLMEmbedder(Embedder):
    name = "minilm"

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        # Runtime must not touch the network; setup downloads the model once.
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name, device=device)
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: list[str]) -> np.ndarray:
        v = self.model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
        return np.asarray(v, dtype=np.float32)


_default: Embedder | None = None


def get_embedder(prefer: str = "auto") -> Embedder:
    """MiniLM when installed and cached locally, else the hashing fallback."""
    global _default
    if prefer == "hashing":
        return HashingEmbedder()
    if _default is not None:
        return _default
    if prefer in ("auto", "minilm"):
        try:
            _default = MiniLMEmbedder()
            return _default
        except Exception:
            if prefer == "minilm":
                raise
    _default = HashingEmbedder()
    return _default
