# Numbers

This document defines the numeric model.

## Domains

- INT: mathematical integers (implementation uses Python int)
- DEC: decimal numbers (implementation uses Python float)

## Operators

- `+`, `−`, `×`, `÷`, `%` follow the interpreter/VM implementation.

## Determinism note

Floating-point behavior follows Python float semantics on the host; this is deterministic for a fixed platform/toolchain but may differ across platforms.
This is a reproducibility consideration, not an equivalence loophole: both backends share the same host model.
