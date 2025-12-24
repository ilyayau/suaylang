# Determinism statement (v0.1)

Normative references:

- docs/LANGUAGE_REFERENCE.md (evaluation order and semantics)
- docs/DIAGNOSTICS_CONTRACT.md (diagnostic determinism)

## Statement

For the supported language subset and under the observation policy, SuayLang is intended to be deterministic:

- Given the same source text, the same commit, and the same runtime environment, evaluation produces the same observed outcome (value/error/stdout) for both the interpreter and the VM.

## Scope

- This statement is about language-level determinism for programs without external nondeterministic inputs.
- Timing measurements (benchmarks) are expected to vary across machines.
