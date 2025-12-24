# Roadmap (research-first)

This roadmap focuses on research-grade evidence, reproducibility, and reviewer experience.
It does not propose new language features.

For an executable Top-20 + milestone breakdown, see docs/EXECUTION_PLAN.md.

## Next release (0.1.x)

- Expand interpreter↔VM conformance corpus and tighten equivalence reporting.
- Add bounded generative differential testing over a larger VM-supported subset.
- Fill micro-benchmark suite with representative, documented programs.
- Improve documentation consistency and reviewer path.

## Medium term

- Improve tooling robustness (LSP performance and diagnostics quality) without expanding semantics.
- Add optional ASCII surface experiment scaffolding (controlled comparison; semantics fixed).
- Increase VM subset coverage (compiler support) while maintaining conformance evidence.

## Out of scope (not a commitment)

- Static typing
- Concurrency
- Macros/metaprogramming
- Large standard library
