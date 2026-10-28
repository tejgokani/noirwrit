import numpy as np
import pytest
import torch

from noirwrit.model.gpt import GPT, PRESETS, GPTConfig, KVCache, build

SMALL = GPTConfig(vocab_size=512, n_layer=2, n_head=4, d_model=64, ffn_hidden=128, ctx_len=64)


def test_preset_sizes():
    sizes = {name: GPT(cfg).num_params() for name, cfg in PRESETS.items() if name != "base"}
    assert 4e6 < sizes["tiny"] < 6e6
    assert 25e6 < sizes["small"] < 40e6


@pytest.mark.slow
def test_base_size():
    n = build("base").num_params()
    assert 90e6 < n < 110e6


def test_forward_and_loss():
    m = GPT(SMALL)
    x = torch.randint(0, 512, (2, 32))
    y = torch.randint(0, 512, (2, 32))
    logits, loss = m(x, y)
    assert logits.shape == (2, 32, 512)
    # Untrained loss on random targets should be close to ln(vocab).
    assert abs(loss.item() - np.log(512)) < 0.5


def test_weights_tied():
    m = GPT(SMALL)
    assert m.lm_head.weight.data_ptr() == m.embed_tokens.weight.data_ptr()


def test_kv_cache_matches_full_forward():
    torch.manual_seed(0)
    m = GPT(SMALL).eval()
    x = torch.randint(0, 512, (1, 20))
    with torch.no_grad():
        full, _ = m(x, x)  # all positions
        cache = KVCache(SMALL, 1, SMALL.ctx_len, "cpu", torch.float32)
        # Prefill 12 tokens, then decode the rest one at a time.
        out, _ = m(x[:, :12], cache=cache, pos=0)
        assert torch.allclose(out[0, -1], full[0, 11], atol=1e-4)
        for t in range(12, 20):
            out, _ = m(x[:, t:t + 1], cache=cache, pos=t)
            assert torch.allclose(out[0, -1], full[0, t], atol=1e-4)


def test_causal():
    torch.manual_seed(0)
    m = GPT(SMALL).eval()
    a = torch.randint(0, 512, (1, 16))
    b = a.clone()
    b[0, 10:] = (b[0, 10:] + 1) % 512
    with torch.no_grad():
        la, _ = m(a, a)
        lb, _ = m(b, b)
    assert torch.allclose(la[0, :10], lb[0, :10], atol=1e-5)
    assert not torch.allclose(la[0, 10:], lb[0, 10:])


def test_overfits_tiny_batch():
    torch.manual_seed(0)
    m = GPT(SMALL)
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3)
    x = torch.randint(0, 512, (4, 32))
    first = None
    for _ in range(60):
        _, loss = m(x[:, :-1], x[:, 1:])
        first = first or loss.item()
        opt.zero_grad()
        loss.backward()
        opt.step()
    assert loss.item() < first * 0.3
