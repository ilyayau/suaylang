# Executive Summary

## Motivation

Programming language backends (interpreters, VMs) are rarely evaluated for strict observational equivalence under a fixed, auditable policy. This project addresses the gap by providing a reproducible, hypothesis-driven artifact for backend equivalence and diagnostics contract.

## Method

- Deterministic, multi-seed differential testing
- Golden diagnostics contract
- Coverage and ablation studies
- All results are saved as artifacts and reproducible by `make reproduce`

## Results

| Metric                | Value | Artifact/Link |
|-----------------------|-------|--------------|
| Seeds                 | 10    | [manifest.json](../results/manifest.json) |
| Programs              | 5001  | [diff_report.md](../results/diff_report.md) |
| Divergences           | 0     | [diff_report.md](../results/diff_report.md) |
| Coverage (AST/opcode) | 24/20 | [coverage.md](../results/coverage.md) |
| Benchmarks            | 6     | [benchmarks.md](../results/benchmarks.md) |

## Why It Matters

- Demonstrates a reproducible, committee-grade approach to backend equivalence
- All claims are evidenced by deterministic outputs and linked artifacts
- Suitable as a foundation for graduate-level research in PL/compilers
