"""Export a checkpoint to GGUF (llama arch), int8 PyTorch, and HF Llama format.

Usage:
    python -m noirwrit.runtime.export artifacts/tiny/latest.pt --gguf --int8 --hf
    python -m noirwrit.runtime.export artifacts/tiny/latest.pt --gguf --quant Q8_0

GGUF notes: the model uses the Hugging Face rotate-half RoPE layout. llama.cpp's
llama arch expects interleaved pairs, so q and k weights are permuted the same
way llama.cpp's convert_hf_to_gguf.py does it.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

from noirwrit.model.gpt import GPTConfig
from noirwrit.tokenizer.train_tokenizer import SPECIAL_TOKENS, TOKENIZER_PATH


def permute_qk(w: np.ndarray, n_head: int) -> np.ndarray:
    """HF rotate-half layout to GGML interleaved layout (same as llama.cpp's converter)."""
    rows = w.shape[0]
    return w.reshape(n_head, 2, rows // n_head // 2, *w.shape[1:]).swapaxes(1, 2).reshape(w.shape)


def _load(ckpt: Path) -> tuple[GPTConfig, dict[str, torch.Tensor]]:
    state = torch.load(ckpt, map_location="cpu", weights_only=False)
    return GPTConfig(**state["config"]), state["model"]


def export_gguf(ckpt: Path, out: Path, tokenizer_path: Path = TOKENIZER_PATH, name: str = "noirwrit") -> Path:
    import gguf

    cfg, sd = _load(ckpt)
    tok = json.loads(tokenizer_path.read_text())
    vocab: dict[str, int] = tok["model"]["vocab"]
    merges = tok["model"]["merges"]
    merges = [" ".join(m) if isinstance(m, list) else m for m in merges]
    tokens = [""] * cfg.vocab_size
    for t, i in vocab.items():
        if i < cfg.vocab_size:
            tokens[i] = t
    for i, t in enumerate(tokens):
        if not t:
            tokens[i] = f"[PAD{i}]"
    special_ids = {vocab[s] for s in SPECIAL_TOKENS if s in vocab}
    types = [gguf.TokenType.CONTROL if i in special_ids else gguf.TokenType.NORMAL for i in range(cfg.vocab_size)]

    out.parent.mkdir(parents=True, exist_ok=True)
    w = gguf.GGUFWriter(str(out), "llama")
    w.add_name(name)
    w.add_context_length(cfg.ctx_len)
    w.add_embedding_length(cfg.d_model)
    w.add_block_count(cfg.n_layer)
    w.add_feed_forward_length(cfg.ffn_hidden)
    w.add_head_count(cfg.n_head)
    w.add_head_count_kv(cfg.n_head)
    w.add_layer_norm_rms_eps(cfg.norm_eps)
    w.add_rope_dimension_count(cfg.head_dim)
    w.add_rope_freq_base(cfg.rope_theta)
    w.add_vocab_size(cfg.vocab_size)
    w.add_file_type(gguf.LlamaFileType.ALL_F32)

    w.add_tokenizer_model("gpt2")
    w.add_tokenizer_pre("gpt-2")
    w.add_token_list(tokens)
    w.add_token_types(types)
    w.add_token_merges(merges)
    w.add_bos_token_id(vocab["<bos>"])
    w.add_eos_token_id(vocab["<eos>"])
    w.add_pad_token_id(vocab["<pad>"])
    w.add_add_bos_token(False)
    w.add_add_eos_token(False)

    def t(key: str) -> np.ndarray:
        return sd[key].float().numpy()

    w.add_tensor("token_embd.weight", t("embed_tokens.weight"))
    for i in range(cfg.n_layer):
        p = f"layers.{i}."
        b = f"blk.{i}."
        w.add_tensor(b + "attn_norm.weight", t(p + "input_layernorm.weight"))
        w.add_tensor(b + "attn_q.weight", permute_qk(t(p + "self_attn.q_proj.weight"), cfg.n_head))
        w.add_tensor(b + "attn_k.weight", permute_qk(t(p + "self_attn.k_proj.weight"), cfg.n_head))
        w.add_tensor(b + "attn_v.weight", t(p + "self_attn.v_proj.weight"))
        w.add_tensor(b + "attn_output.weight", t(p + "self_attn.o_proj.weight"))
        w.add_tensor(b + "ffn_norm.weight", t(p + "post_attention_layernorm.weight"))
        w.add_tensor(b + "ffn_gate.weight", t(p + "mlp.gate_proj.weight"))
        w.add_tensor(b + "ffn_up.weight", t(p + "mlp.up_proj.weight"))
        w.add_tensor(b + "ffn_down.weight", t(p + "mlp.down_proj.weight"))
    w.add_tensor("output_norm.weight", t("norm.weight"))
    # Tied embeddings: llama.cpp reuses token_embd when output.weight is absent,
    # but writing it explicitly keeps every llama.cpp version happy.
    w.add_tensor("output.weight", t("lm_head.weight") if "lm_head.weight" in sd else t("embed_tokens.weight"))

    w.write_header_to_file()
    w.write_kv_data_to_file()
    w.write_tensors_to_file()
    w.close()
    return out


def quantize_gguf(src: Path, quant: str = "Q8_0") -> Path:
    exe = shutil.which("llama-quantize")
    if not exe:
        raise RuntimeError("llama-quantize not found; install llama.cpp (brew install llama.cpp)")
    dst = src.with_name(src.stem.replace("-f32", "") + f"-{quant.lower()}.gguf")
    subprocess.run([exe, str(src), str(dst), quant], check=True, capture_output=True)
    return dst


def export_int8(ckpt: Path, out: Path) -> Path:
    """Save a dynamically quantized model (weights only) for the PyTorch runtime."""
    from noirwrit.runtime.engine import load_checkpoint, quantize_int8

    model = load_checkpoint(ckpt, "cpu")
    q = quantize_int8(model)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"config": model.cfg.to_dict(), "int8_state": q.state_dict()}, out)
    return out


def export_hf(ckpt: Path, out_dir: Path, tokenizer_path: Path = TOKENIZER_PATH) -> Path:
    """LlamaForCausalLM layout: config.json, model.safetensors, tokenizer.json."""
    from safetensors.torch import save_file

    cfg, sd = _load(ckpt)
    out_dir.mkdir(parents=True, exist_ok=True)
    hf = {}
    for k, v in sd.items():
        if k == "lm_head.weight" and cfg.tie_embeddings:
            continue
        hf["model." + k if k != "lm_head.weight" else k] = v.contiguous()
    save_file(hf, str(out_dir / "model.safetensors"))
    tok = json.loads(tokenizer_path.read_text())
    vocab = tok["model"]["vocab"]
    (out_dir / "config.json").write_text(json.dumps({
        "architectures": ["LlamaForCausalLM"], "model_type": "llama",
        "vocab_size": cfg.vocab_size, "hidden_size": cfg.d_model, "intermediate_size": cfg.ffn_hidden,
        "num_hidden_layers": cfg.n_layer, "num_attention_heads": cfg.n_head, "num_key_value_heads": cfg.n_head,
        "max_position_embeddings": cfg.ctx_len, "rms_norm_eps": cfg.norm_eps, "rope_theta": cfg.rope_theta,
        "hidden_act": "silu", "tie_word_embeddings": cfg.tie_embeddings, "torch_dtype": "float32",
        "bos_token_id": vocab["<bos>"], "eos_token_id": vocab["<eos>"], "pad_token_id": vocab["<pad>"],
    }, indent=2))
    shutil.copy(tokenizer_path, out_dir / "tokenizer.json")
    return out_dir


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ckpt")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--name", default="noirwrit")
    ap.add_argument("--gguf", action="store_true")
    ap.add_argument("--quant", default="", help="llama-quantize type, e.g. Q8_0 or Q4_K_M")
    ap.add_argument("--int8", action="store_true")
    ap.add_argument("--hf", action="store_true")
    a = ap.parse_args(argv)
    ckpt = Path(a.ckpt)
    out_dir = Path(a.out_dir) if a.out_dir else ckpt.parent / "export"
    if a.gguf:
        g = export_gguf(ckpt, out_dir / f"{a.name}-f32.gguf", name=a.name)
        print("gguf:", g)
        if a.quant:
            print("quantized:", quantize_gguf(g, a.quant))
    if a.int8:
        print("int8:", export_int8(ckpt, out_dir / f"{a.name}-int8.pt"))
    if a.hf:
        print("hf:", export_hf(ckpt, out_dir / "hf"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
