.PHONY: install test lint format format-check smoke build check conformance fuzz bench golden contract diff-test diff-test-ci human-study bench-report research research-pdf

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

diff-test:
	$(PY) -m tools.diff_test.main --profile full --out-dir results

diff-test-ci:
	$(PY) -m tools.diff_test.main --profile ci --out-dir results

golden:
	$(PY) -m pytest -q tests/test_golden_diagnostics.py tests/test_golden_error_codes.py

contract:
	$(PY) tools/decisions/generate_decision_log.py --check

bench:
	$(PY) benchmarks/benchmark_runner.py --profile full --out-dir results

bench-report:
	$(PY) benchmarks/benchmark_runner.py --profile full --out-dir results

human-study:
	$(PY) -m tools.human_proxy.run --out-dir results

research-pdf:
	$(PY) tools/build_research_plan_pdf.py


research:
	$(PY) -m tools.research_run --out-dir results --diff-profile ci --bench-profile smoke
	$(PY) experiments/baseline_runner.py

smoke:
	$(PY) scripts/smoke.py

build:
	$(PY) -m build

tr:
	pandoc paper/TR-2025-01.md -o paper/TR-2025-01.pdf \
	  --defaults=paper/pandoc_tr_pdf_args.txt || \
	  pandoc paper/TR-2025-01.md -o paper/TR-2025-01.pdf \
	    --pdf-engine=xelatex --toc --number-sections --highlight-style=tango

check: lint format-check test smoke build
