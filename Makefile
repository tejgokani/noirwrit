PY ?= $(HOME)/.local/bin/python3.11
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup test lint run monitor

setup:
	uv venv --python $(PY) $(VENV)
	uv pip install --python $(BIN)/python -e ".[dev,data,embed,export]"

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
