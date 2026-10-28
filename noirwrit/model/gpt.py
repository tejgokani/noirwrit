"""Decoder-only GPT written from scratch, Llama-compatible layout.

RoPE (rotate-half form, as in Hugging Face Llama), RMSNorm, SwiGLU MLP, tied
input and output embeddings, scaled_dot_product_attention, and a KV cache for
inference. Parameter names follow the HF Llama layout so the export to a
LlamaForCausalLM checkpoint (and from there to GGUF) is a rename, not a rewrite.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class GPTConfig:
    vocab_size: int = 16384
    n_layer: int = 12
    n_head: int = 12
    d_model: int = 768
    ffn_hidden: int = 2048
    ctx_len: int = 2048
    rope_theta: float = 10000.0
    norm_eps: float = 1e-5
    dropout: float = 0.0
    tie_embeddings: bool = True

    @property
    def head_dim(self) -> int:
        return self.d_model // self.n_head

    def to_dict(self) -> dict:
        return asdict(self)


PRESETS: dict[str, GPTConfig] = {
    # ~5M params. Local smoke tests on the Mac.
    "tiny": GPTConfig(n_layer=4, n_head=4, d_model=192, ffn_hidden=512, ctx_len=512),
    # ~34M params.
    "small": GPTConfig(n_layer=8, n_head=8, d_model=512, ffn_hidden=1408, ctx_len=2048),
    # ~98M params. The main model.
    "base": GPTConfig(n_layer=12, n_head=12, d_model=768, ffn_hidden=2048, ctx_len=2048),
}


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        x = x.float()
        x = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return self.weight * x.to(dtype)


def rope_cache(head_dim: int, max_len: int, theta: float, device=None) -> tuple[torch.Tensor, torch.Tensor]:
    inv = 1.0 / (theta ** (torch.arange(0, head_dim, 2, device=device).float() / head_dim))
    t = torch.arange(max_len, device=device).float()
    freqs = torch.outer(t, inv)
    emb = torch.cat([freqs, freqs], dim=-1)
    return emb.cos(), emb.sin()


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat([-x2, x1], dim=-1)


def apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    # x: (B, H, T, D); cos, sin: (T, D)
    return x * cos + rotate_half(x) * sin


class KVCache:
    """Preallocated per-layer key and value buffers for incremental decoding."""

    def __init__(self, cfg: GPTConfig, batch: int, max_len: int, device, dtype):
        shape = (batch, cfg.n_head, max_len, cfg.head_dim)
        self.k = [torch.zeros(shape, device=device, dtype=dtype) for _ in range(cfg.n_layer)]
        self.v = [torch.zeros(shape, device=device, dtype=dtype) for _ in range(cfg.n_layer)]
        self.max_len = max_len


class Attention(nn.Module):
    def __init__(self, cfg: GPTConfig):
        super().__init__()
        self.cfg = cfg
        d = cfg.d_model
        self.q_proj = nn.Linear(d, d, bias=False)
        self.k_proj = nn.Linear(d, d, bias=False)
        self.v_proj = nn.Linear(d, d, bias=False)
        self.o_proj = nn.Linear(d, d, bias=False)

    def forward(self, x, cos, sin, cache: KVCache | None = None, layer: int = 0, pos: int = 0):
        B, T, _ = x.shape
        H, D = self.cfg.n_head, self.cfg.head_dim
        q = self.q_proj(x).view(B, T, H, D).transpose(1, 2)
        k = self.k_proj(x).view(B, T, H, D).transpose(1, 2)
        v = self.v_proj(x).view(B, T, H, D).transpose(1, 2)
        q = apply_rope(q, cos, sin)
        k = apply_rope(k, cos, sin)
        if cache is not None:
            cache.k[layer][:B, :, pos:pos + T] = k
            cache.v[layer][:B, :, pos:pos + T] = v
            k = cache.k[layer][:B, :, : pos + T]
            v = cache.v[layer][:B, :, : pos + T]
            if T == 1:
                y = F.scaled_dot_product_attention(q, k, v)
            else:
                # Causal mask offset by the cached prefix.
                mask = torch.ones(T, pos + T, dtype=torch.bool, device=x.device).tril(diagonal=pos)
                y = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
        else:
            drop = self.cfg.dropout if self.training else 0.0
            y = F.scaled_dot_product_attention(q, k, v, is_causal=True, dropout_p=drop)
        y = y.transpose(1, 2).reshape(B, T, H * D)
        return self.o_proj(y)


class MLP(nn.Module):
    def __init__(self, cfg: GPTConfig):
        super().__init__()
        self.gate_proj = nn.Linear(cfg.d_model, cfg.ffn_hidden, bias=False)
        self.up_proj = nn.Linear(cfg.d_model, cfg.ffn_hidden, bias=False)
        self.down_proj = nn.Linear(cfg.ffn_hidden, cfg.d_model, bias=False)

    def forward(self, x):
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))


class Block(nn.Module):
    def __init__(self, cfg: GPTConfig):
        super().__init__()
        self.input_layernorm = RMSNorm(cfg.d_model, cfg.norm_eps)
        self.self_attn = Attention(cfg)
        self.post_attention_layernorm = RMSNorm(cfg.d_model, cfg.norm_eps)
        self.mlp = MLP(cfg)

    def forward(self, x, cos, sin, cache=None, layer=0, pos=0):
        x = x + self.self_attn(self.input_layernorm(x), cos, sin, cache, layer, pos)
        return x + self.mlp(self.post_attention_layernorm(x))


class GPT(nn.Module):
    def __init__(self, cfg: GPTConfig):
        super().__init__()
        self.cfg = cfg
        self.embed_tokens = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.layers = nn.ModuleList(Block(cfg) for _ in range(cfg.n_layer))
        self.norm = RMSNorm(cfg.d_model, cfg.norm_eps)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        if cfg.tie_embeddings:
            self.lm_head.weight = self.embed_tokens.weight
        cos, sin = rope_cache(cfg.head_dim, cfg.ctx_len, cfg.rope_theta)
        self.register_buffer("rope_cos", cos, persistent=False)
        self.register_buffer("rope_sin", sin, persistent=False)
        self.apply(self._init)
        # Scale residual output projections by depth (GPT-2 style).
        for name, p in self.named_parameters():
            if name.endswith("o_proj.weight") or name.endswith("down_proj.weight"):
                nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * cfg.n_layer))

    @staticmethod
    def _init(m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)

    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None,
                cache: KVCache | None = None, pos: int = 0):
        B, T = idx.shape
        if pos + T > self.cfg.ctx_len:
            raise ValueError(f"sequence {pos + T} exceeds ctx_len {self.cfg.ctx_len}")
        x = self.embed_tokens(idx)
        cos = self.rope_cos[pos:pos + T].to(x.dtype)
        sin = self.rope_sin[pos:pos + T].to(x.dtype)
        for i, layer in enumerate(self.layers):
            x = layer(x, cos, sin, cache, i, pos)
        x = self.norm(x)
        if targets is not None:
            logits = self.lm_head(x)
            loss = F.cross_entropy(logits.float().reshape(-1, logits.size(-1)), targets.reshape(-1), ignore_index=-1)
            return logits, loss
        # Inference only needs the last position.
        return self.lm_head(x[:, -1:, :]), None

    def configure_optimizer(self, lr: float, weight_decay: float, betas=(0.9, 0.95), device_type: str = "cpu"):
        decay, no_decay = [], []
        for p in self.parameters():
            if not p.requires_grad:
                continue
            (decay if p.dim() >= 2 else no_decay).append(p)
        groups = [
            {"params": decay, "weight_decay": weight_decay},
            {"params": no_decay, "weight_decay": 0.0},
        ]
        fused = device_type == "cuda"
        return torch.optim.AdamW(groups, lr=lr, betas=betas, fused=fused)


def build(preset_or_cfg: str | GPTConfig | dict, **overrides) -> GPT:
    if isinstance(preset_or_cfg, str):
        cfg = GPTConfig(**{**PRESETS[preset_or_cfg].to_dict(), **overrides})
    elif isinstance(preset_or_cfg, dict):
        cfg = GPTConfig(**{**preset_or_cfg, **overrides})
    else:
        cfg = GPTConfig(**{**preset_or_cfg.to_dict(), **overrides})
    return GPT(cfg)
