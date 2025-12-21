# Results Folder Guide

This folder contains all experiment outputs, metrics, and evidence artifacts for SuayLang artifact evaluation.

## Structure

## How to read

## Reproduce
Run `make reproduce-all` from repo root. All outputs will be regenerated and checksummed.

# Results Folder Guide & Artifact Index

This folder contains all experiment outputs, metrics, and evidence artifacts for SuayLang artifact evaluation. Every file is directly referenced from the main claim, and all results are reproducible by running the pipeline.

## Artifact Summary Table

| Artifact                | File(s)                        | Purpose / Evidence                                      |
|-------------------------|--------------------------------|---------------------------------------------------------|
| Diff test report        | diff_report.md, diff_report.json| Main equivalence evidence (0 divergences)               |
| Baseline comparison     | baseline.md, baseline_raw.json  | Baseline timings, reference outputs                     |
| Coverage report         | coverage.md, coverage.json      | AST/opcode coverage metrics                             |
| Benchmarks              | benchmarks.md, bench_raw.json   | Runtime performance evidence                            |
| Diagnostics contract    | golden_diagnostics.md, .json    | Error contract, diagnostics evidence                    |
| Ablation/mutation       | ablation.md, mutation_catches.md| Robustness, mutation/injection validation               |
| Manifest/environment    | manifest.json, environment.json | Seeds, commit hash, environment metadata                |
| Human study proxy       | human_study.md, human_study.csv | Human-facing proxy evidence (if present)                |

## Reviewer Artifact Index

- [Diff test report](diff_report.md)
- [Coverage report](coverage.md)
- [Baseline comparison](baseline.md)
- [Benchmarks](benchmarks.md)
- [Diagnostics contract](golden_diagnostics.md)
- [Ablation results](ablation.md)
- [Mutation catch results](mutation_catches.md)
- [Manifest/environment](manifest.json), (environment.json)
- [Claim–Evidence matrix](../docs/CLAIM_EVIDENCE_MATRIX.md)
- [Reviewer portal](../docs/REVIEWER_PORTAL.md)
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
