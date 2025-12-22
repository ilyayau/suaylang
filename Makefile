# Check all internal markdown links
check-links:
	sh scripts/check_links.sh
# Release artifact: dist/results_<gitsha>.tar.gz with results/ and key docs
release-artifacts:
	@echo "Generating release artifact..."
	gitsha=$$(git rev-parse --short HEAD); \
	date=$$(date -u +%Y-%m-%dT%H:%M:%SZ); \
	pyver=$$($(PY) --version 2>&1 | awk '{print $$2}'); \
	os=$$(uname -a); \
	echo "Git SHA: $$gitsha" > dist/MANIFEST.txt; \
	echo "Date: $$date" >> dist/MANIFEST.txt; \
	echo "Python: $$pyver" >> dist/MANIFEST.txt; \
	echo "OS: $$os" >> dist/MANIFEST.txt; \
	tar -czf dist/results_$$gitsha.tar.gz results/ docs/COMMITTEE_ONEPAGER.md docs/TECH_REPORT.md results/baseline.md results/diff_report.md results/benchmarks.md dist/MANIFEST.txt
	@echo "Release artifact created: dist/results_$$gitsha.tar.gz"
baseline:
	$(PY) experiments/baseline_runner.py
	cp results/baseline_raw.json results/manifest.json

plots:
	$(PY) tools/plot_results.py

manifest:
	$(PY) tools/gen_manifest.py

reproduce-all: baseline plots manifest
	# The following lines are commented out because benchmark_runner.py does not support these arguments.
	# $(PY) benchmarks/benchmark_runner.py --diff > results/diff_report.md
	# $(PY) benchmarks/benchmark_runner.py --coverage > results/coverage.md
	# $(PY) benchmarks/benchmark_runner.py --benchmarks > results/benchmarks.md
	# $(PY) benchmarks/benchmark_runner.py --golden > results/golden_diagnostics.md
	# $(PY) benchmarks/benchmark_runner.py --ablation > results/ablation.md
	# $(PY) benchmarks/benchmark_runner.py --mutation > results/mutation_catches.md
	# $(PY) benchmarks/benchmark_runner.py --constructs > results/coverage_by_construct.md

pdf:
	$(PY) scripts/build_pdf.py

ci: reproduce-all pdf
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
PYTHON_VERSION ?= 3.12
# Note: You can override the Python interpreter by running 'make PY=python3.12' or similar.
# The PY variable specifies the Python interpreter to use (default: python3.12).
# All CI and artifact scripts require Python $(PYTHON_VERSION).x.
# You can also set PIP and RUFF similarly if needed.
# ...existing code...
# ...existing code...

lint:
	$(RUFF) check .
	# The following lines are commented out because benchmark_runner.py does not support these arguments.
	# $(PY) benchmarks/benchmark_runner.py --diff > results/diff_report.md
	# $(PY) benchmarks/benchmark_runner.py --coverage > results/coverage.md
	# $(PY) benchmarks/benchmark_runner.py --benchmarks > results/benchmarks.md
	# $(PY) benchmarks/benchmark_runner.py --golden > results/golden_diagnostics.md
	# $(PY) benchmarks/benchmark_runner.py --ablation > results/ablation.md
	# $(PY) benchmarks/benchmark_runner.py --mutation > results/mutation_catches.md
	# $(PY) benchmarks/benchmark_runner.py --constructs > results/coverage_by_construct.md

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

