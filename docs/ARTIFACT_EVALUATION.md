# Artifact Evaluation Guide (AE)

## Prerequisites
- OS: Linux (tested), Python 3.13.11
- RAM: >=2GB, Disk: >=1GB free
- Git, make, pip

## Step-by-step Reproduction
1. Clone repo: `git clone https://github.com/ilyayau/suaylang && cd suaylang`
2. Run: `./scripts/reproduce.sh` (fast) or `./scripts/reproduce.sh --full` (full)
3. Inspect outputs: `results/README.md`, `results/diff_report.md`, `results/baseline.md`, `results/benchmarks.md`
4. For Windows: use `scripts/reproduce.ps1`

## Expected Outputs
- All results in `results/` (see `results/README.md`)
- Key metrics: see output of `python scripts/extract_metrics.py`
- PDFs: `paper/suaylang-tech-report.pdf` (if generated)

## Sanity Checks
- All commands exit 0
- `REPRODUCED OK` is printed
- Results files are non-empty and match those in CI artifact

## Time Budget Table
| Mode      | Command                      | Time   |
|-----------|------------------------------|--------|
| Fast      | ./scripts/reproduce.sh       | <10min |
| Full      | ./scripts/reproduce.sh --full| <20min |

## Determinism Notes
- All experiments use fixed seeds, commit hash, and environment capture
- Results are reproducible on supported OS/Python
