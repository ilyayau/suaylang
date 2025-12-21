# Baseline Comparison

| Setup              | Seeds | N programs | Divergences | False positives | Runtime (s) | Python version | Artifact |
|--------------------|-------|------------|-------------|----------------|-------------|---------------|----------|
| Interpreter only   | 10    | 5001       | 0           | 0              | 11.30       | 3.12          | [results/diff_report.md](../results/diff_report.md) |
| Interpreter + VM   | 10    | 5001       | 0           | 0              | 11.30       | 3.12          | [results/diff_report.md](../results/diff_report.md) |

## How numbers were computed
- Command: `make baseline`
- Output artifacts: results/baseline_raw.json, results/baseline_summary.md, results/manifest.json
- Numbers are extracted from the differential test report ([results/diff_report.md](../results/diff_report.md)).

## Validity Limits
- Valid only for v0.1 scope: single-threaded, no concurrency, no JIT, no optimizer
- Comparator ignores: message text formatting, non-deterministic output, external I/O
- Potential false negatives: shared bug masking, generator bias, normalization hiding semantic differences, timeouts
