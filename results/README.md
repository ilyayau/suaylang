# Results: Artifact Index

This directory is the committee-facing index of **generated evidence artifacts**.

All files here are produced by a documented command and are referenced by reviewer docs.

## Reproduce

Fast (PR/push, intended ≤5 minutes):

```sh
make reproduce-fast
```

Full (nightly/dispatch, slower):

```sh
make reproduce-all
```

If results diverge (or artifacts are missing), follow: docs/REPRODUCIBILITY.md

## Integrity metadata

- results/manifest.json — per-file SHA-256 and environment metadata for this run.
- results/hashes.txt — SHA-256 list over a broader reviewer-facing set.

You can verify a produced manifest locally via:

```sh
make verify-results
```

## Key artifacts (common)

| Artifact | File(s) | Purpose |
|---|---|---|
| Baseline suite | baseline.md, baseline_raw.json | per-program median timings (machine-dependent) |
| Equivalence report | diff_report.md, diff_report.json | divergence summary and counterexample (when failing) |
| Corpus coverage | coverage.json, coverage.md, coverage_by_construct.md | feature/opcode/corpus summaries used for evaluation |
| Plots (results) | img/performance.png, img/coverage.png | figures derived from generated JSON artifacts |

## Notes

- Numeric values are not asserted in docs; docs link to these artifacts.
- This folder may contain additional reports depending on the pipeline profile.
