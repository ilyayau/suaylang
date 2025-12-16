# Conformance tooling (scaffold)

This folder will contain tooling to evaluate *observational equivalence* between:
- the reference interpreter (baseline semantics), and
- the bytecode compiler + VM (engineering artifact).

## Goal

Provide hard, reproducible evidence that the VM matches the interpreter on a documented subset.

## What must match (planned observational equivalence)

For programs in the supported subset, compare:
- Termination kind: success vs user-facing error (lex/syntax/runtime)
- Stdout: exact text printed (normalize newlines)
- On error: category and span/location when available

## What is not guaranteed

- Exact wording of error messages
- Exact stack trace shape/frames
- Equivalence outside the documented VM-supported subset

## Status

This is scaffolding only. Implementation will live in run.py.
