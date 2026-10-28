# Contributing to Noirwrit

Thanks for helping. Noirwrit is a small, offline project, so the bar is simple: keep it local, keep it legal, keep it light on a laptop.

## Setup

```bash
make setup
source .venv/bin/activate
pytest
```

## Rules

- Training data must be public domain in the US. Every new source goes in `data/SOURCES.md` with its ID, author, first publication year, and the basis for the public domain call. If you are not sure, leave it out.
- The app must make zero network calls at runtime. Downloads belong in setup or data scripts only.
- Heavy local jobs run through `tools/guard.py`. Do not add code that trains large models on a laptop by default.
- Run `ruff check .` and `pytest` before opening a pull request.
- Plain, direct docs and comments.

## Pull requests

One topic per pull request. Describe what changed, why, and how you tested it.
