# Evaluation protocol (standalone)

This doc is the committee-facing entrypoint for “what to run” and “what to inspect”.

## One command

```sh
make reproduce-all
```

## What it runs

- Baseline suite: `make baseline` → results/baseline_raw.json + results/baseline.md
- Plots: `make plots` → docs/plots/performance.png and docs/plots/interp_vs_vm.png
- Microbench plot: `make plot-microbench` → docs/plots/microbench_relative.png
- Integrity metadata: `make manifest` and `make hashes`

## Equivalence testing

- Protocol definition: docs/EXPERIMENT_PROTOCOL.md
- CI subset: `make diff-test-ci`
- Full run: `make diff-test`

## How to interpret outcomes

- Pass: artifacts exist and tests succeed.
- Fail: a counterexample divergence is a falsification signal and should be recorded as a regression.

See also: docs/EVIDENCE_MAP.md and results/README.md.
