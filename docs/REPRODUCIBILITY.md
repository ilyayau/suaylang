# Reproducibility (Committee Contract)

This document defines the **canonical reproduction command**, the **expected artifacts**, and what to do **if results diverge**.

## Canonical command

From repo root:

```sh
make reproduce-all
```

This target generates the artifact index under results/ and produces integrity metadata.

## Expected artifacts

After `make reproduce-all`, you should be able to inspect:

- results/README.md (artifact index)
- results/baseline.md and results/baseline_raw.json
- results/manifest.json (commit + environment + hashes for selected artifacts)
- results/hashes.txt (SHA-256 over a broader evidence set)

Plots for the report-facing documents:

- docs/plots/microbench_relative.png (derived from benchmarks/results.md)
- docs/plots/performance.png and docs/plots/coverage.png (derived from results/baseline_raw.json)

## If results diverge

First, confirm you are running the supported environment:

- Linux + Python 3.12.x

Then:

1) Clean outputs:
```sh
rm -rf results/ docs/plots/
```

2) Re-run:
```sh
make reproduce-all
```

3) Inspect integrity metadata:
- Compare results/manifest.json and results/hashes.txt between runs.
- If hashes differ, identify which artifact differs first (do not compare screenshots).

4) File a reproducibility report:
- Use the template under results/independent_reproduction/receipt_template.md
- Attach your results/manifest.json and results/hashes.txt

## Independent reproduction (placeholder)

This repo includes a structured place to record independent reproductions:

- results/independent_reproduction/

Committee reviewers can drop a minimal receipt there without changing code.