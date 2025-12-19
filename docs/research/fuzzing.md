# Differential fuzzing (interpreter ↔ VM)

## Goal

Generate many small Suay programs and compare **observations** (termination kind, stdout, value/effect, error location) between:

- the reference interpreter, and
- the bytecode compiler + VM.

Any divergence is treated as a bug.

## Determinism

Fuzz generation is deterministic per seed. Seed lists are stored in:

- `tools/conformance/fuzz_seeds.json`

## CI gate vs full run

CI gate (small, fast):

```sh
python -m tools.conformance.fuzz_matrix --profile ci --n 5000
```

Nightly (research evidence run):

```sh
python -m tools.conformance.fuzz_matrix --profile nightly --n 10000 \
  --json-out docs/research/raw_results/fuzz_nightly.json
```

This yields $10 \times 10{,}000 = 100{,}000$ generated programs per nightly run.

## Regression corpus

- Divergence repros are saved under `tools/conformance/fuzz_failures/`.
- Minimal retained regressions live under `tools/conformance/regressions/` and are executed in CI:

```sh
python -m tools.conformance.run_regressions
```

## Current status

- Fixed conformance suite: 50 programs
- Regression divergences retained: 0
