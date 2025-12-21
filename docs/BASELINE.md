# Baseline Comparison

| Setup              | Seeds | N programs | Divergences caught | False positives | Runtime (s) | Artifact |
|--------------------|-------|------------|-------------------|----------------|-------------|----------|
| Interpreter only   | 10    | 5001       | 0                 | 0              | 11.30       | [results/diff_report.md](../results/diff_report.md) |
| Interpreter + VM   | 10    | 5001       | 0                 | 0              | 11.30       | [results/diff_report.md](../results/diff_report.md) |

## How numbers were computed
- Command: `make research`
- Output artifact: results/diff_report.md
- Numbers are extracted from the differential test report (see [results/diff_report.md](../results/diff_report.md)).

## Validity/Limitations
- Valid only for v0.1 scope: single-threaded, no concurrency, no JIT, no optimizer.
- Comparator ignores: message text formatting, non-deterministic output, external I/O.
- Potential false negatives: shared bug masking, generator bias, normalization hiding semantic differences, timeouts.
