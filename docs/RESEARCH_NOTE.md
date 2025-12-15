# Research Note (for academic review)

## Problem statement

Many language prototypes emphasize syntax features before they demonstrate **deterministic semantics**, **diagnostics**, and a **repeatable evaluation path**. For review and research contexts, the question is less “does it have features?” and more:

- Can the semantics be explained precisely?
- Can failures be reported with actionable source locations?
- Can the implementation be evaluated quickly and reproduced on a clean machine?

SuayLang is a small language prototype that treats those as first-class constraints.

## Motivation

This project explores an implementation approach where “control flow is explicit and expression-oriented”:

- Branching and looping are expressed via explicit constructs (`dispatch`, `cycle`) rather than implicit statements.
- State change is visually distinct (binding vs mutation).
- The same surface programs can be executed both by a reference interpreter and by a minimal bytecode VM.

The goal is not ecosystem completeness; it is to create a compact artifact suitable for reasoning, teaching, and review.

## Novelty and design choices

SuayLang’s novelty is primarily in the *combination* of constraints rather than new theoretical primitives:

- **Control-flow as data-shape selection**: `dispatch` and `cycle` both select behavior via pattern matching.
- **Explicit state machine loops**: `cycle` makes the “state” and transitions visible.
- **Dual execution paths**: interpreter as reference, plus a stack VM to test semantic drift.
- **Span-based diagnostics**: lexer/parser/runtime errors are intended to be human-readable and location-specific.

## Implementation method

The implementation is intentionally straightforward and reviewer-friendly:

- Lexer → Parser → AST with spans
- Interpreter (reference semantics)
- Compiler → bytecode
- Stack-based VM (subset, designed to mirror interpreter semantics)

## Evaluation approach

Evaluation is based on reproducible checks rather than subjective claims:

- Unit + stress tests (`pytest -q`).
- Smoke checks running canonical examples and verifying stdout (`python scripts/smoke.py`).
- Lint/format consistency (`ruff`).
- Packaging build reproducibility (`python -m build`).
- Interpreter vs VM equivalence tests on a supported subset (including property-based tests).

## Limitations

- The VM is intentionally minimal and may not cover every language construct.
- The standard library is small by design.
- Performance is not the primary objective; the benchmark script is provided for honest measurement, not marketing.

## Future work

- Extend equivalence coverage between interpreter and VM for more constructs.
- Improve static tooling (LSP features) and error explanations.
- Add a small, curated corpus for regression testing and teaching.
