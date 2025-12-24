# Error model (v0.1)

Normative references:

- docs/ERROR_CODES.md (stable codes)
- docs/DIAGNOSTICS_CONTRACT.md (invariants)

## Categories

- Lexical errors (E-LEX, E-ESC)
- Syntax errors (E-SYNTAX)
- Runtime errors (E-NAME, E-NOMATCH, E-TYPE, E-DIV0, E-STACK, ...)
- Host/IO errors (E-UTF8, module load failures)

## Determinism

- Diagnostic codes are stable by contract.
- Diagnostics are deterministic for a given input and commit (see docs/DIAGNOSTICS_CONTRACT.md).

## Spans

- Diagnostics include spans anchored to the relevant token/character (see error code catalog).
