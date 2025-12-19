# Differential fuzz regressions

This directory is a checked-in regression corpus for **interpreter ↔ VM divergences** found by
`python -m tools.conformance.fuzz` / `python -m tools.conformance.fuzz_matrix`.

- Each subdirectory should contain a `program.suay` repro and an `observations.json` snapshot.
- Regressions are executed in CI via `python -m tools.conformance.run_regressions`.

## Status

- Bugs found (divergences): 0
- Bugs fixed and retained as regressions: 0

When a divergence is found, preserve it here (don’t delete) so that future changes can’t reintroduce it.
