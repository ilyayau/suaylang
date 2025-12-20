# Experiments: Reproducible Evaluation

This directory contains the scripts and instructions for running all core experiments and regenerating results artifacts.

## How to run

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest -q
make research
```

## What is measured
- Interpreter↔VM equivalence (differential testing)
- Diagnostics stability (golden tests)
- Coverage (AST/opcode kinds)
- Benchmarks (median/p90 timings)
- Environment metadata (Python, OS, CPU, commit)

## What “success” means
- 0 divergences in diff_report
- 100% diagnostic stability in golden diagnostics
- Coverage ≥24 AST node kinds, ≥20 opcode kinds
- Benchmarks: all programs run, timings reported
- All results/ artifacts are regenerated deterministically

## Protocol
- Deterministic by seed
- Multi-seed profiles: CI (0..9), local full (0..99)
- Size buckets: S/M/L
- Minimization: if divergence found, shrink and store minimal repro in results/regressions/

---

**See also:**
- [../results/README.md](../results/README.md)
- [../docs/RESEARCH.md](../docs/RESEARCH.md)
