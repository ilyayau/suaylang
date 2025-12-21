# Results index (SuayLang)

This directory contains all reviewer-facing, reproducible research artifacts.

## Main results artifacts

- Differential test report: [diff_report.md](diff_report.md), [diff_report.json](diff_report.json)
- Coverage report: [coverage.md](coverage.md), [coverage.json](coverage.json)
- Benchmarks: [benchmarks.md](benchmarks.md), [bench_raw.json](bench_raw.json)
- Golden diagnostics: [golden_diagnostics.md](golden_diagnostics.md), [golden_diagnostics.json](golden_diagnostics.json)
- Environment metadata: [environment.md](environment.md), [environment.json](environment.json)
- Human-facing proxy: [human_study.md](human_study.md), [human_study.csv](human_study.csv)
- Baseline comparison: [baseline.md](baseline.md)
- Ablation results: [ablation.md](ablation.md)
- Coverage by construct: [coverage_by_construct.md](coverage_by_construct.md)
- Mutation catch results: [mutation_catches.md](mutation_catches.md)

## Results Directory

- **diff_report.md**: Divergences between interpreter and VM (should be 0 for all seeds/programs)
- **coverage.md**: Coverage metrics for AST and opcode kinds
- **benchmarks.md**: Runtime benchmarks for baseline programs
- **baseline.md**: Baseline comparison table
- **ablation.md**: Ablation study table
- **golden_diagnostics.md**: Diagnostics contract results
- **manifest.json**: Seeds, commit hash, environment metadata
- ***.json**: Raw outputs for reproducibility

## How to Read
- All metrics are deterministic and reproducible
- Each file is referenced from the main report and claims mapping
- manifest.json records the exact environment for this artifact

## How to reproduce results exactly

```sh
make research
```

All files are generated deterministically by `make research`.
