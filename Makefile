reproduce:
	$(PY) -m pytest -q
	$(PY) tools/conformance/run.py
	$(PY) tools/conformance/run.py conformance/corpus
	$(PY) -m tools.diff_test.main --profile ci --out-dir results
	$(PY) experiments/baseline_runner.py
	$(PY) benchmarks/benchmark_runner.py --profile full --out-dir results
	$(PY) experiments/ablation_runner.py
	make research-pdf
	make tech-report-pdf
tech-report-pdf:
	pandoc paper/tech_report.md -o paper/suaylang-tech-report.pdf \
	  --defaults=paper/pandoc_tr_pdf_args.txt || \
	  pandoc paper/tech_report.md -o paper/suaylang-tech-report.pdf \
	    --pdf-engine=xelatex --toc --number-sections --highlight-style=tango
.PHONY: install test lint format format-check smoke build check conformance fuzz bench golden contract diff-test diff-test-ci human-study bench-report research research-pdf

PY ?= python3
PIP ?= pip
RUFF ?= ruff

install:
	$(PY) -m venv .venv
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e ".[dev]"
# Note: You can override the Python interpreter by running 'make PY=python3.12' or similar.
# The PY variable specifies the Python interpreter to use.
# Default is set to python3 if not overridden.
# You can also set PIP and RUFF similarly if needed.
# ...existing code...
# ...existing code...

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
