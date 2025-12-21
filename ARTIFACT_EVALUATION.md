# Artifact Evaluation Guide

## Hardware/Software Assumptions
- Linux (x86_64), Python 3.12+, `make`, `pandoc`, `pytest`, `pip install -e .`

## Step-by-Step Reproduction
1. Clone the repository and checkout the evaluated commit.
2. Run `make install` to set up the environment.
3. Run `make reproduce` to execute all tests, conformance, diff-test, baseline, ablation, and build PDFs.
4. Inspect `results/` for all output artifacts (see [results/README.md](results/README.md)).
5. For research plan PDF: `make research-pdf` (output in `docs/`).

## Expected outputs
- All results in `results/` (see `results/README.md`)
- Key metrics: `python scripts/extract_metrics.py`
- Tech report: [docs/TECH_REPORT.md](docs/TECH_REPORT.md) (PDF: run `make tech-report-pdf`)

## Time Budget
- Full run: ~15 minutes on a modern laptop.

## Sanity Checks
- If results differ: check Python version, OS, and commit hash.
- If any artifact is missing or malformed, rerun `make reproduce` and check logs.
- For persistent issues, see [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md).

## Main Claim Verification
- Confirm that `results/diff_report.md` shows 0 divergences.
- Confirm that coverage and diagnostics match the summary in README.
- All outputs should be versioned and cross-linked.
