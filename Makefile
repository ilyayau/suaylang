
PY ?= python

.PHONY: reproduce-all baseline plots plot-microbench manifest hashes check-links \
	pytest conformance fuzz diff-test diff-test-ci golden contract bench research \
	smoke build tech-report-pdf release-artifacts

# Link checker (reviewer UX)
check-links:
	sh scripts/check_links.sh

# Canonical artifact pipeline
baseline:
	$(PY) experiments/baseline_runner.py

plot-microbench:
	$(PY) tools/plot_microbench.py --in-md benchmarks/results.md --out docs/plots/microbench_relative.png

plots: plot-microbench
	$(PY) tools/plot_results.py

manifest:
	$(PY) tools/gen_manifest.py

hashes:
	$(PY) tools/gen_hashes.py

reproduce-all: baseline plots manifest hashes
	@echo "[ok] reproduce-all completed"

# Tests and research utilities
pytest:
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

research:
	$(PY) -m tools.research_run --out-dir results --diff-profile ci --bench-profile smoke
	$(PY) experiments/baseline_runner.py

smoke:
	$(PY) scripts/smoke.py

build:
	$(PY) -m build

# Optional: PDF generation (requires pandoc + LaTeX)
tech-report-pdf:
	pandoc paper/tech_report.md -o paper/suaylang-tech-report.pdf \
	  --defaults=paper/pandoc_tr_pdf_args.txt || \
	  pandoc paper/tech_report.md -o paper/suaylang-tech-report.pdf \
	    --pdf-engine=xelatex --toc --number-sections --highlight-style=tango

# Optional: release artifact bundle
release-artifacts:
	@mkdir -p dist
	@echo "Generating release artifact..."
	gitsha=$$(git rev-parse --short HEAD); \
	date=$$(date -u +%Y-%m-%dT%H:%M:%SZ); \
	pyver=$$($(PY) --version 2>&1 | awk '{print $$2}'); \
	os=$$(uname -a); \
	echo "Git SHA: $$gitsha" > dist/MANIFEST.txt; \
	echo "Date: $$date" >> dist/MANIFEST.txt; \
	echo "Python: $$pyver" >> dist/MANIFEST.txt; \
	echo "OS: $$os" >> dist/MANIFEST.txt; \
	tar -czf dist/results_$$gitsha.tar.gz results/ docs/COMMITTEE_ONEPAGER.md docs/TECH_REPORT.md dist/MANIFEST.txt
	@echo "Release artifact created: dist/results_$$gitsha.tar.gz"

