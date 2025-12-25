# Determinism

## Guarantee

The SuayLang artifact is intended to be deterministic for a fixed:

- program text
- spec version (spec/VERSION)
- implementation commit

Determinism is required for reproducible artifacts (manifest + hashes).

## What is included in determinism

- Evaluation order is fixed (spec/eval_order.md).
- Truthiness and numeric operations follow the specified rules.
- Pattern matching and dispatch/cycle selection are deterministic.

## What is excluded

- Wall-clock timing values are machine-dependent and are not part of semantics.
- Any host-level I/O outside stdout/stderr is out of scope.

## Falsifier

If `make reproduce-all` produces different semantic observations for the same input program on the same commit/spec version, that is a determinism bug.
