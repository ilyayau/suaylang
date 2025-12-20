# Release experiments (SuayLang)

This document tracks version evolution as a sequence of research experiments.

## v0.1 (baseline)
- Naive interpreter, minimal corpus, no VM.
- No diagnostics contract.
- No coverage reporting.

## v0.2
- Generator upgrade: multi-seed scaling, stratified program sizes.
- Initial VM implementation and diff-test harness.
- Coverage reporting (AST/opcode kinds).

## v0.3
- Diagnostic contract: golden diagnostics, error-code mapping.
- Minimization and regression corpus for divergences.
- Benchmarks: smoke suite, environment metadata.

## v1.0
- Defined observation policy (see [docs/SPEC_V1_SCOPE.md](SPEC_V1_SCOPE.md)).
- Stable contract: interpreter↔VM equivalence, diagnostics, coverage.
- Reproducible protocol: `make research` generates all results/ artifacts.
- Reviewer path and artifact bundle.

---

**See also:**
- [CHANGELOG.md](../CHANGELOG.md)
- [docs/METRICS.md](METRICS.md)
- [docs/RESEARCH_CLAIM.md](RESEARCH_CLAIM.md)
