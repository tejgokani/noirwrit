VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup model tools demo test lint run monitor

# One command from a fresh clone: make setup && make model && make demo
setup:
	@command -v uv >/dev/null || { echo "Install uv first: brew install uv"; exit 1; }
	@command -v llama-completion >/dev/null || echo "Tip: brew install llama.cpp for fast Metal generation (PyTorch is used otherwise)."
	@brew list pango >/dev/null 2>&1 || echo "Tip: brew install pango for PDF export (WeasyPrint)."
	uv venv --python 3.11 $(VENV)
	uv pip install --python $(BIN)/python -e ".[dev,data,export,train]"

# Install the model: this checkout's trained weights if present, else the release on Hugging Face.
model:
	$(BIN)/noirwrit install-model

# Optional: epubcheck for EPUB validation (needs Java).
tools:
	mkdir -p $(HOME)/.noirwrit/tools && cd $(HOME)/.noirwrit/tools && \
	curl -sSLO https://github.com/w3c/epubcheck/releases/download/v5.4.0/epubcheck-5.4.0.zip && \
	unzip -q -o epubcheck-5.4.0.zip && rm epubcheck-5.4.0.zip

demo:
	$(BIN)/noirwrit demo

test:
	$(BIN)/pytest -q

lint:
	$(BIN)/ruff check .

run:
	$(BIN)/noirwrit serve

monitor:
	$(BIN)/python tools/monitor.py --interval 30

.PHONY: train-online train-status bench samples serve-dev
train-online:
	uv pip install --python $(BIN)/python -q kaggle
	$(BIN)/python tools/online/kaggle_train.py

train-status:
	$(BIN)/python tools/online/kaggle_train.py --status

bench:
	$(BIN)/python tools/guard.py --timeout-min 10 -- $(BIN)/python tools/bench.py

samples:
	$(BIN)/python tools/guard.py --timeout-min 10 -- $(BIN)/python tools/samples.py
