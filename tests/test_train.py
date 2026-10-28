import json

import numpy as np
import torch

from noirwrit.train import train as T


def _fake_shards(tmp_path, vocab=300, n=20000):
    rng = np.random.default_rng(0)
    # A repeating pattern is easy to learn, so the loss should fall fast.
    base = rng.integers(0, vocab, size=97)
    data = np.tile(base, n // 97 + 1)[:n].astype(np.uint16)
    for s in ("general", "crime", "noir"):
        data.tofile(tmp_path / f"{s}_train.bin")
        data[:4000].tofile(tmp_path / f"{s}_val.bin")
    return tmp_path


def _args(tmp_path, out, extra=()):
    return [
        "--preset", "tiny", "--ctx", "64", "--shards", str(tmp_path), "--out", str(out),
        "--micro-batch", "4", "--max-steps", "60", "--eval-every", "20", "--eval-iters", "2",
        "--sample-every", "0", "--warmup", "5", "--device", "cpu", "--lr", "3e-3", *extra,
    ]


def _log(out):
    return [json.loads(line) for line in (out / "train_log.jsonl").read_text().splitlines()]


def test_lr_schedule():
    assert T.lr_at(0, 100, 10, 1.0, 0.1) == 0.1
    assert abs(T.lr_at(10, 100, 10, 1.0, 0.1) - 1.0) < 1e-9
    assert abs(T.lr_at(100, 100, 10, 1.0, 0.1) - 0.1) < 1e-9


def test_parse_stages():
    st = T.parse_stages("general:1:1,crime:3:1,noir:1:0.3:es")
    assert [s.name for s in st] == ["general", "crime", "noir"]
    assert abs(sum(s.share for s in st) - 1) < 1e-9
    assert st[2].early_stop and st[2].lr_scale == 0.3


def test_training_reduces_loss_and_resumes(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "maybe_push_hub", lambda *a, **k: None)
    shards = tmp_path / "shards"
    shards.mkdir()
    _fake_shards(shards)
    out = tmp_path / "run"
    # Vocab of the tiny preset is 16384; data only uses ids < 300, which is fine.
    assert T.main(_args(shards, out)) == 0
    log = _log(out)
    losses = [r["loss"] for r in log if "loss" in r]
    assert losses[-1] < losses[0] * 0.6
    done = [r for r in log if r.get("event") == "done"][-1]
    assert done["step"] == 60

    ck = torch.load(out / "latest.pt", weights_only=False)
    assert ck["step"] == 60

    # Resume and extend to 80 steps.
    assert T.main(_args(shards, out, ["--resume", str(out / "latest.pt"), "--max-steps", "80"])) == 0
    log = _log(out)
    resumed = [r for r in log if r.get("event") == "resumed"]
    assert resumed and resumed[-1]["step"] == 60
    assert [r for r in log if r.get("event") == "done"][-1]["step"] == 80


def test_budget_stop(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "maybe_push_hub", lambda *a, **k: None)
    shards = tmp_path / "shards"
    shards.mkdir()
    _fake_shards(shards)
    out = tmp_path / "run"
    # Absurd hourly rate so the budget trips on the first logged step.
    T.main(_args(shards, out, ["--cost-per-hour", "1000000", "--budget-usd", "0.01"]))
    done = [r for r in _log(out) if r.get("event") == "done"][-1]
    assert done["reason"] == "budget"
