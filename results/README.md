# Results index (SuayLang)

This directory contains all reviewer-facing, reproducible research artifacts.

## Main results artifacts

- Differential test report: [diff_report.md](diff_report.md), [diff_report.json](diff_report.json)
- Coverage report: [coverage.md](coverage.md), [coverage.json](coverage.json)
- Benchmarks: [benchmarks.md](benchmarks.md), [bench_raw.json](bench_raw.json)
- Golden diagnostics: [golden_diagnostics.md](golden_diagnostics.md), [golden_diagnostics.json](golden_diagnostics.json)
- Environment metadata: [environment.md](environment.md), [environment.json](environment.json)
- Human-facing proxy: [human_study.md](human_study.md), [human_study.csv](human_study.csv)
- Baseline comparison: [baseline.md](baseline.md)  # TODO: to be created in next step


## Artifact summary table

| Artifact         | Description                        | Format(s)         |
|-----------------|------------------------------------|-------------------|
| diff_report      | Differential test results          | .md, .json        |
| coverage         | AST/opcode coverage                | .md, .json        |
| benchmarks       | Microbenchmark suite               | .md, .json        |
| golden_diagnostics | Golden diagnostics test results  | .md, .json        |
| environment      | Python/OS/CPU metadata             | .md, .json        |
| human_study      | Proxy static metrics               | .md, .csv         |
| baseline         | Baseline comparison (see below)    | .md               |

## Baseline results table (stub)

| Approach         | Correctness (%) | Diagnostic stability (%) | Coverage (node kinds) | Notes |
|------------------|----------------:|------------------------:|----------------------:|-------|
| Naive interpreter| TODO            | TODO                   | TODO                 |       |
| Current interp/VM| TODO            | TODO                   | TODO                 |       |
| Raw-string diag  | TODO            | TODO                   | TODO                 |       |
| Structured diag  | TODO            | TODO                   | TODO                 |       |

See [baseline.md](baseline.md) for details. This table will be updated as soon as the baseline runner is implemented.

All files are generated deterministically by `make research`.
