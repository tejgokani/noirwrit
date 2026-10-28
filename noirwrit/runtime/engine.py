"""PyTorch inference engine: KV cache, streaming, sampling controls, int8.

Sampling controls: temperature, top-k, top-p, repetition penalty, and a
no-repeat n-gram ban. Long generations slide the window: when the cache is
full, the engine re-prefills from the last `ctx_len - keep_room` tokens.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import torch

from noirwrit.model.gpt import GPT, GPTConfig, KVCache


@dataclass
class SampleParams:
    max_new_tokens: int = 400
    temperature: float = 0.85
    top_k: int = 0
    top_p: float = 0.92
    repetition_penalty: float = 1.15
    rep_window: int = 256
    no_repeat_ngram: int = 4
    stop_ids: tuple[int, ...] = ()
    seed: int | None = None


def load_checkpoint(path: str | Path, device: str = "cpu") -> GPT:
    state = torch.load(path, map_location="cpu", weights_only=False)
    model = GPT(GPTConfig(**state["config"]))
    model.load_state_dict(state["model"])
    return model.to(device).eval()


def quantize_int8(model: GPT) -> torch.nn.Module:
    """Dynamic int8 quantization of all Linear layers (CPU backend).

    The tied lm_head shares storage with the embedding, so it is untied first
    and kept in float; quantizing it would also quantize the embedding.
    """
    model = model.cpu().eval()
    if model.lm_head.weight is model.embed_tokens.weight:
        model.lm_head.weight = torch.nn.Parameter(model.embed_tokens.weight.detach().clone())
    try:
        engine = "qnnpack" if "qnnpack" in torch.backends.quantized.supported_engines else None
        if engine:
            torch.backends.quantized.engine = engine
    except Exception:
        pass
    qmods = {torch.nn.Linear}
    q = torch.ao.quantization.quantize_dynamic(model, qmods, dtype=torch.qint8)
    # Keep the output head in float for quality.
    q.lm_head = model.lm_head
    return q


def _banned_ngram_tokens(seq: list[int], n: int) -> set[int]:
    if n <= 1 or len(seq) < n - 1:
        return set()
    prefix = tuple(seq[-(n - 1):])
    banned = set()
    for i in range(len(seq) - n + 1):
        if tuple(seq[i:i + n - 1]) == prefix:
            banned.add(seq[i + n - 1])
    return banned


def sample_next(logits: torch.Tensor, history: list[int], p: SampleParams, gen: torch.Generator | None) -> int:
    logits = logits.float().clone()
    if p.repetition_penalty and p.repetition_penalty != 1.0 and history:
        recent = torch.tensor(sorted(set(history[-p.rep_window:])), dtype=torch.long)
        vals = logits[recent]
        logits[recent] = torch.where(vals > 0, vals / p.repetition_penalty, vals * p.repetition_penalty)
    if p.no_repeat_ngram:
        # Only scan a bounded tail so long chapters stay fast.
        banned = _banned_ngram_tokens(history[-1024:], p.no_repeat_ngram)
        if banned:
            logits[list(banned)] = -float("inf")
    if p.temperature <= 0:
        return int(torch.argmax(logits))
    logits = logits / p.temperature
    if p.top_k:
        v, _ = torch.topk(logits, min(p.top_k, logits.numel()))
        logits[logits < v[-1]] = -float("inf")
    probs = torch.softmax(logits, -1)
    if p.top_p and p.top_p < 1.0:
        sp, si = torch.sort(probs, descending=True)
        cum = torch.cumsum(sp, -1)
        cut = cum - sp > p.top_p
        sp[cut] = 0
        probs = torch.zeros_like(probs).scatter_(0, si, sp)
        probs = probs / probs.sum()
    return int(torch.multinomial(probs, 1, generator=gen))


class Engine:
    """Streaming generator over a GPT (float or int8)."""

    def __init__(self, model: torch.nn.Module, device: str = "cpu", keep_room: int = 512):
        self.model = model
        self.cfg: GPTConfig = model.cfg
        self.device = device
        self.keep_room = min(keep_room, self.cfg.ctx_len // 2)
        self.dtype = next(model.parameters()).dtype if any(True for _ in model.parameters()) else torch.float32
        self.last_stats: dict = {}

    @classmethod
    def from_checkpoint(cls, path: str | Path, device: str = "cpu", int8: bool = False) -> Engine:
        m = load_checkpoint(path, "cpu" if int8 else device)
        if int8:
            return cls(quantize_int8(m), "cpu")
        return cls(m, device)

    @torch.no_grad()
    def stream(self, prompt_ids: list[int], params: SampleParams | None = None) -> Iterator[int]:
        p = params or SampleParams()
        gen = None
        if p.seed is not None:
            gen = torch.Generator().manual_seed(p.seed)
        ctx = self.cfg.ctx_len
        history = list(prompt_ids)
        # Leave room to generate before the first slide.
        window = history[-(ctx - self.keep_room):] or [0]
        cache = KVCache(self.cfg, 1, ctx, self.device, torch.float32)
        x = torch.tensor([window], device=self.device)
        t0 = time.perf_counter()
        logits, _ = self.model(x, cache=cache, pos=0)
        pos = len(window)
        t_prefill = time.perf_counter() - t0
        produced = 0
        t1 = time.perf_counter()
        while produced < p.max_new_tokens:
            nxt = sample_next(logits[0, -1].cpu(), history, p, gen)
            history.append(nxt)
            produced += 1
            yield nxt
            if nxt in p.stop_ids:
                break
            if pos >= ctx:
                window = history[-(ctx - self.keep_room):]
                cache = KVCache(self.cfg, 1, ctx, self.device, torch.float32)
                logits, _ = self.model(torch.tensor([window], device=self.device), cache=cache, pos=0)
                pos = len(window)
                continue
            logits, _ = self.model(torch.tensor([[nxt]], device=self.device), cache=cache, pos=pos)
            pos += 1
        dt = time.perf_counter() - t1
        self.last_stats = {
            "prompt_tokens": len(prompt_ids), "new_tokens": produced,
            "prefill_s": round(t_prefill, 4), "decode_s": round(dt, 4),
            "tok_per_s": round(produced / dt, 2) if dt > 0 else 0.0,
        }

    def generate(self, prompt_ids: list[int], params: SampleParams | None = None) -> list[int]:
        return list(self.stream(prompt_ids, params))
