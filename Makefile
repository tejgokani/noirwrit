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
