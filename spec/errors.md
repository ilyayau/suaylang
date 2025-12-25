# Errors (semantic contract)

Errors are part of semantics: termination class, code, and span policy are observable per the observation policy.

## Error classes

- Lexical errors: invalid tokenization or invalid escapes.
- Syntax errors: parse failure.
- Runtime errors: name errors, type errors, division by zero, pattern-match failure, etc.

## Stable codes

Stable error codes are defined in docs/ERROR_CODES.md.

## Span policy

Span/caret placement is defined in docs/DIAGNOSTICS_CONTRACT.md.

## Falsifier

If interpreter and VM disagree on error code or span for the same program in the shipped corpora, `results/diff_report.*` must record the counterexample.
