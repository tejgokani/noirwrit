"""Text generators the story engine can drive.

All implement `generate(prompt, max_tokens, seed, on_token) -> (text, tokens)`.
- TorchGenerator: Noirwrit checkpoint through the PyTorch engine (float or int8).
- LlamaCppGenerator: GGUF through llama.cpp (llama-completion / llama-cli), Metal on the Mac.
- EchoGenerator: deterministic stand-in for tests; no model needed.
"""

from __future__ import annotations

import random
import re
import shutil
import subprocess
import time
from collections.abc import Callable
from pathlib import Path

OnToken = Callable[[str], None] | None


class Generator:
    name = "base"
    tok_per_s: float = 0.0

    def generate(self, prompt: str, max_tokens: int, seed: int = 0, on_token: OnToken = None) -> tuple[str, int]:
        raise NotImplementedError

    def count_tokens(self, text: str) -> int:
        return max(1, int(len(text.split()) * 1.3))


class TorchGenerator(Generator):
    name = "torch"

    def __init__(self, ckpt: str | Path, device: str = "cpu", int8: bool = True, **sample_kw):
        from noirwrit.runtime.engine import Engine, SampleParams
        from noirwrit.tokenizer.train_tokenizer import load_tokenizer

        self.tok = load_tokenizer()
        self.engine = Engine.from_checkpoint(ckpt, device=device, int8=int8)
        self.SampleParams = SampleParams
        self.sample_kw = sample_kw
        self.eos = self.tok.token_to_id("<eos>")

    def count_tokens(self, text: str) -> int:
        return len(self.tok.encode(text).ids)

    def generate(self, prompt, max_tokens, seed=0, on_token=None):
        ids = self.tok.encode(prompt).ids
        params = self.SampleParams(max_new_tokens=max_tokens, seed=seed, stop_ids=(self.eos,), **self.sample_kw)
        out: list[int] = []
        emitted = ""
        for t in self.engine.stream(ids, params):
            if t == self.eos:
                break
            out.append(t)
            if on_token:
                # Decode incrementally so multi-byte tokens come out whole.
                text = self.tok.decode(out)
                if len(text) > len(emitted) and not text.endswith("�"):
                    on_token(text[len(emitted):])
                    emitted = text
        self.tok_per_s = self.engine.last_stats.get("tok_per_s", 0.0)
        return self.tok.decode(out), len(out)


class LlamaCppGenerator(Generator):
    """Runs a GGUF with llama.cpp in a subprocess. Offline, Metal accelerated."""

    name = "llama.cpp"

    def __init__(self, gguf: str | Path, threads: int = 4, temperature: float = 0.85, top_p: float = 0.92,
                 repeat_penalty: float = 1.15, ctx: int = 2048):
        self.gguf = str(gguf)
        self.exe = shutil.which("llama-completion") or shutil.which("llama-cli")
        if not self.exe:
            raise RuntimeError("llama.cpp not found")
        self.args = ["-t", str(threads), "--temp", str(temperature), "--top-p", str(top_p),
                     "--repeat-penalty", str(repeat_penalty), "-c", str(ctx)]

    def generate(self, prompt, max_tokens, seed=0, on_token=None):
        cmd = [self.exe, "-m", self.gguf, "-p", prompt, "-n", str(max_tokens), "-s", str(seed or 1),
               "--no-display-prompt", "-no-cnv", *self.args]
        t0 = time.perf_counter()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, errors="replace", bufsize=1)
        assert proc.stdout is not None
        parts = []
        while True:
            ch = proc.stdout.read(64)
            if not ch:
                break
            parts.append(ch)
            if on_token:
                on_token(ch)
        proc.wait()
        text = "".join(parts).replace("[end of text]", "").strip()
        n = self.count_tokens(text)
        self.tok_per_s = n / max(time.perf_counter() - t0, 1e-6)
        return text, n


class EchoGenerator(Generator):
    """Deterministic fake model: recombines sentences from a seed text.

    Fast and reproducible, which is what the end-to-end tests need. It can also
    inject a planted error for consistency tests.
    """

    name = "echo"
    SOURCE = (
        "The rain had not stopped since noon. I lit a cigarette and watched the street below. "
        "Nobody in this town told the truth unless it was cheaper than a lie. "
        "The door opened and the cold came in with her. She had the kind of face that cost men money. "
        "I asked where she had been that night, and she looked at the window instead of at me. "
        "Somewhere a radio was playing a song I had stopped liking years ago. "
        "The lieutenant chewed his cigar and said the case was closed. I said it had never been open. "
        "There was blood on the stair, dried brown, and a smell of gin in the hall. "
        "I put my hat on and went out into the wet dark to find someone who would talk."
    )

    def __init__(self, tok_per_s: float = 5000.0, inject: str = "", simulate_speed: bool = False):
        self.sentences = [s.strip() + "." for s in self.SOURCE.split(".") if s.strip()]
        self.tok_per_s = tok_per_s
        self.inject = inject
        # When set, sleep as a real model would at tok_per_s (worker and ETA tests).
        self.simulate_speed = simulate_speed

    def generate(self, prompt, max_tokens, seed=0, on_token=None):
        rng = random.Random(seed or hash(prompt) & 0xFFFF)
        words = []
        if self.inject:
            words.extend(self.inject.split())
        while len(words) * 1.3 < max_tokens:
            words.extend(rng.choice(self.sentences).split())
        text = " ".join(words)
        # Paragraphs every few sentences.
        text = re.sub(r"(\.)\s+(?=[A-Z])", lambda m, c=[0]: ".\n\n" if (c.__setitem__(0, c[0] + 1) or c[0] % 4 == 0) else ". ", text)
        n = self.count_tokens(text)
        if on_token or self.simulate_speed:
            words = text.split(" ")
            step = self.simulate_speed and n / self.tok_per_s / max(len(words), 1)
            for w in words:
                if on_token:
                    on_token(w + " ")
                if step:
                    time.sleep(step)
        return text, n
