.PHONY: install test lint format format-check smoke build check conformance fuzz bench golden contract

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

conformance:
	$(PY) tools/conformance/run.py
	$(PY) tools/conformance/run.py conformance/corpus

fuzz:
	$(PY) -m tools.conformance.fuzz --seed 0 --n 1000

golden:
	$(PY) -m pytest -q tests/test_golden_diagnostics.py tests/test_golden_error_codes.py

contract:
	$(PY) tools/decisions/generate_decision_log.py --check

bench:
	$(PY) scripts/bench_micro.py --iters 200 benchmarks

smoke:
	$(PY) scripts/smoke.py

build:
	$(PY) -m build

check: lint format-check test smoke build
