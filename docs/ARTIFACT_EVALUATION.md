# Artifact Evaluation Guide (AE)

## Prerequisites
- OS: Linux (tested), Python 3.13.11
- RAM: >=2GB, Disk: >=1GB free
- Git, make, pip

## Fast path vs full path
| Mode      | Command                      | Time   |
|-----------|------------------------------|--------|
| Fast      | ./scripts/reproduce.sh       | <10min |
| Full      | ./scripts/reproduce.sh --full| <20min |

## Step-by-step reproduction
1. Clone: `git clone https://github.com/ilyayau/suaylang && cd suaylang`
2. Run: `./scripts/reproduce.sh` (or `--full`)
3. Inspect: [results/README.md](../results/README.md), [results/diff_report.md](../results/diff_report.md), [results/baseline.md](../results/baseline.md), [results/benchmarks.md](../results/benchmarks.md)
4. For Windows: use `scripts/reproduce.ps1`

## Expected outputs
- All results in `results/` (see `results/README.md`)
- Key metrics: `python scripts/extract_metrics.py`
- Tech report: [docs/TECH_REPORT.md](../docs/TECH_REPORT.md) (if generated: run `make tech-report-pdf`)

## Sanity checks
- All commands exit 0
- `REPRODUCED OK` is printed
- Results files are non-empty and match those in CI artifact
