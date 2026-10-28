import shutil
import subprocess

import numpy as np
import pytest
import torch

from noirwrit.model.gpt import GPT, GPTConfig
from noirwrit.runtime.engine import (
    Engine,
    SampleParams,
    _banned_ngram_tokens,
    quantize_int8,
    sample_next,
)
from noirwrit.runtime.export import permute_qk

CFG = GPTConfig(vocab_size=300, n_layer=2, n_head=4, d_model=64, ffn_hidden=128, ctx_len=48)


def _model(seed=0):
    torch.manual_seed(seed)
    return GPT(CFG).eval()


def test_greedy_engine_matches_full_forward():
    m = _model()
    prompt = [5, 9, 13, 2]
    out = Engine(m).generate(prompt, SampleParams(max_new_tokens=10, temperature=0, repetition_penalty=1.0, no_repeat_ngram=0))
    # Recompute greedily without a cache.
    seq = list(prompt)
    with torch.no_grad():
        for _ in range(10):
            logits, _ = m(torch.tensor([seq]))
            seq.append(int(logits[0, -1].argmax()))
    assert out == seq[len(prompt):]


def test_streaming_slides_past_context():
    m = _model()
    e = Engine(m, keep_room=16)
    out = list(e.stream([1, 2, 3], SampleParams(max_new_tokens=120, seed=1)))
    assert len(out) == 120  # far beyond ctx_len=48
    assert e.last_stats["new_tokens"] == 120


def test_seeded_sampling_is_reproducible():
    m = _model()
    p = SampleParams(max_new_tokens=20, seed=42)
    assert Engine(m).generate([4, 5], p) == Engine(m).generate([4, 5], p)


def test_no_repeat_ngram_bans_continuation():
    hist = [1, 2, 3, 9, 1, 2]
    assert _banned_ngram_tokens(hist, 3) == {3}
    logits = torch.zeros(10)
    logits[3] = 100.0
    p = SampleParams(temperature=0, repetition_penalty=1.0, no_repeat_ngram=3)
    assert sample_next(logits, hist, p, None) != 3


def test_repetition_penalty_lowers_recent_tokens():
    logits = torch.tensor([2.0, 2.0, 0.0])
    p = SampleParams(temperature=0, repetition_penalty=2.0, no_repeat_ngram=0)
    assert sample_next(logits, [0], p, None) == 1


def test_top_p_restricts_to_nucleus():
    logits = torch.log(torch.tensor([0.6, 0.3, 0.05, 0.05]))
    p = SampleParams(temperature=1.0, top_p=0.5, repetition_penalty=1.0, no_repeat_ngram=0)
    g = torch.Generator().manual_seed(0)
    assert {sample_next(logits, [], p, g) for _ in range(50)} == {0}


def test_int8_close_to_float():
    m = _model()
    x = torch.randint(0, 300, (1, 24))
    with torch.no_grad():
        ref, _ = m(x, x)
    q = quantize_int8(_model())
    with torch.no_grad():
        got, _ = q(x, x)
    cos = torch.nn.functional.cosine_similarity(ref.flatten(), got.flatten(), dim=0)
    assert cos > 0.99


def test_permute_qk_matches_llama_cpp_layout():
    # Reference: llama.cpp convert_hf_to_gguf permute().
    n_head, head_dim, d = 2, 4, 8
    w = np.arange(d * d, dtype=np.float32).reshape(d, d)
    ref = w.reshape(n_head, 2, head_dim // 2, d).swapaxes(1, 2).reshape(d, d)
    assert np.array_equal(permute_qk(w, n_head), ref)
    # Row 1 of the permuted head 0 comes from the second half of head 0 (rotate-half pair).
    assert np.array_equal(permute_qk(w, n_head)[1], w[2])


@pytest.mark.skipif(not shutil.which("llama-completion"), reason="llama.cpp not installed")
def test_gguf_greedy_matches_torch(tmp_path):
    from noirwrit.runtime.export import export_gguf
    from noirwrit.tokenizer.train_tokenizer import TOKENIZER_PATH, load_tokenizer

    if not TOKENIZER_PATH.exists():
        pytest.skip("tokenizer not trained")
    tok = load_tokenizer()
    torch.manual_seed(3)
    cfg = GPTConfig(vocab_size=tok.get_vocab_size(), n_layer=2, n_head=4, d_model=128, ffn_hidden=256, ctx_len=128)
    m = GPT(cfg).eval()
    # Sharpen the random model so greedy picks are not near ties.
    with torch.no_grad():
        m.embed_tokens.weight.mul_(8)
    ck = tmp_path / "m.pt"
    torch.save({"model": m.state_dict(), "config": cfg.to_dict(), "step": 0}, ck)
    g = export_gguf(ck, tmp_path / "m.gguf")
    prompt = "The fog came in over the harbor and"
    ids = tok.encode(prompt).ids
    torch_out = tok.decode(Engine(m).generate(ids, SampleParams(max_new_tokens=12, temperature=0, repetition_penalty=1.0, no_repeat_ngram=0)))
    r = subprocess.run(["llama-completion", "-m", str(g), "-p", prompt, "-n", "12", "--temp", "0", "--repeat-penalty", "1.0",
                        "-s", "1", "--no-display-prompt", "-no-cnv"], capture_output=True, text=True, timeout=120)
    assert r.stdout.strip().startswith(torch_out.strip()[:30])
