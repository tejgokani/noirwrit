import json

import numpy as np
import pytest

from noirwrit.tokenizer import train_tokenizer as TT

pytestmark = pytest.mark.skipif(not TT.TOKENIZER_PATH.exists(), reason="tokenizer not trained yet")


def test_special_tokens_reserved():
    tok = TT.load_tokenizer()
    assert tok.get_vocab_size() == TT.VOCAB_SIZE
    assert [tok.token_to_id(s) for s in TT.SPECIAL_TOKENS] == list(range(len(TT.SPECIAL_TOKENS)))


@pytest.mark.parametrize("text", [
    '"You\'re late," said Spade. The fog rolled in off the bay.',
    "Mr. Holmes, they were the footprints of a gigantic hound!",
    "Line one.\n\nLine two -- with   odd   spacing\tand tabs.\n",
    "Café, naïve, Zoë: accents survive the round trip.",
    "1929. $4,000 in small bills; 3:15 a.m.",
])
def test_round_trip(text):
    tok = TT.load_tokenizer()
    assert tok.decode(tok.encode(text).ids) == text


def test_tokens_per_word_under_target():
    tok = TT.load_tokenizer()
    text = (
        "The night was cold and the street was empty. I walked to the corner and lit a cigarette, "
        "watching the window across the way. Somebody had killed the old man for money, and somebody "
        "was going to pay for it before the morning came."
    )
    ratio = len(tok.encode(text).ids) / len(text.split())
    assert ratio < 1.4


def test_shards_are_uint16_with_eos():
    meta_path = TT.SHARDS / "meta.json"
    if not meta_path.exists():
        pytest.skip("shards not packed yet")
    meta = json.loads(meta_path.read_text())
    eos = meta["eos"]
    for s in TT.SETS:
        tr = np.memmap(TT.SHARDS / f"{s}_train.bin", dtype=np.uint16, mode="r")
        assert len(tr) == meta["counts"][s]["train"]
        assert tr.max() < meta["vocab_size"]
        assert eos in tr[-1:]
