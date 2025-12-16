# Micro-benchmarks (scaffold)

These benchmarks are designed to support research evaluation of SuayLang’s VM as an engineering artifact.

## Philosophy

- Compare **interpreter vs VM** on the same SuayLang programs.
- Report **relative** performance only (no cross-language speed claims).
- Prefer small, explainable programs over large workloads.
- Control or avoid I/O during timing (stdout dominates otherwise).
- Use median/min/max across many iterations.

## Layout

- benchmarks/dispatch/: dispatch-heavy programs
- benchmarks/cycle/: cycle-heavy state machines
- benchmarks/calls/: function-call-heavy programs
- benchmarks/mixed/: mixed workloads

## Status

Scaffold only: program files and measurement scripts will be added later.
