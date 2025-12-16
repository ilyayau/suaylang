# Testing pyramid (v0.1)

SuayLang aims for reviewer-friendly assurance without relying on large, slow test infrastructure.

## Layers

1) **Unit tests** (`tests/`)
   - lexer/parser correctness
   - interpreter semantics
   - VM/compiler behavior on supported subset

2) **Conformance corpus** (interpreter ↔ VM)
   - `tests/corpus/conformance/`
   - runner: `python tools/conformance/run.py`

3) **Differential fuzzing** (interpreter ↔ VM)
   - runner: `python -m tools.conformance.fuzz`
   - deterministic via `--seed`

4) **Grammar fuzzing** (parser robustness)
   - `tests/fuzz/test_parser_fuzz.py`
   - goal: lexer/parser never crash/hang on random input

5) **Golden diagnostics** (stable UX)
   - `tests/golden/cases/*.suay` + `*.txt`
   - goal: stable span/caret formatting and messages

## CI budget

CI runs a small fuzz budget to stay fast; reviewers can run larger budgets locally.
