# Evaluation order (v0.1)

Normative reference: docs/LANGUAGE_REFERENCE.md.

## Strictness

- Evaluation is eager (strict) by default.

## Order

- Left-to-right evaluation for operands and arguments.

Exceptions:

- Short-circuit boolean operators (&& / ||) may skip RHS evaluation.
- dispatch and cycle evaluate the scrutinee/seed once; arms are tested top-to-bottom and only the selected arm body is evaluated.
