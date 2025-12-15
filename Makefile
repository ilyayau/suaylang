.PHONY: install test lint format format-check smoke build check

PY := .venv/bin/python
PIP := .venv/bin/pip
RUFF := .venv/bin/ruff

install:
	python -m venv .venv
	$(PIP) install -U pip
	$(PIP) install -e ".[dev]"

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

format-check:
	$(RUFF) format --check .

test:
	$(PY) -m pytest -q

smoke:
	$(PY) scripts/smoke.py

build:
	$(PY) -m build

check: lint format-check test smoke build
