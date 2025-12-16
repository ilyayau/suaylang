# SuayLang error model (minimal, v0.1)

This repo treats errors as part of the user-facing contract.
The CLI must present errors without Python tracebacks.

## Error classes

SuayLang reports errors in these categories:

- **Lexical errors**: invalid characters, malformed literals
- **Syntax errors**: structurally invalid programs
- **Runtime errors**: undefined names, type errors, failed dispatch/cycle, module/link errors
- **Internal errors**: bugs in the implementation (should be rare; still must be user-facing)

## Determinism

Given the same source program and inputs (no external I/O), errors are deterministic:

- the error type is stable
- the (line, column) span anchor is stable
- the primary message is stable

## Location / spans

- Lex and parse errors report `(line, column)` and include a caret line excerpt.
- Runtime errors attach a source span where the error is raised.
- When code uses ASCII aliases, spans are reported against the ASCII source text (same physical offsets the user wrote).

## CLI contract

- User-facing errors must never print a Python traceback.
- The test suite includes golden diagnostics to keep formatting stable.
