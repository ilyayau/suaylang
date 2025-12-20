# Roadmap (research-first)

This roadmap is about making SuayLang *reviewable*:

- a scorable scope statement,
- deterministic evidence generation,
- and controlled risk.

It intentionally deprioritizes “more features” unless they strengthen evidence.

## Near-term (v0.x → v1-scored)

- **Scope freeze for the research claim**: keep [docs/SPEC_V1_SCOPE.md](SPEC_V1_SCOPE.md) aligned with implementation and tests.
- **Observation policy hardening**: expand the stable set of observations (what is compared) only when backed by artifacts.
- **Golden diagnostics expansion**: grow the golden snapshot corpus to cover the stable error codes and common user mistakes.
- **Regression corpus growth**: store minimized divergences (if any) and fixed regressions under version control.
- **Repro runner stability**: keep `make research` producing the same file set under `results/` with environment metadata.

## Mid-term

- **VM subset expansion (evidence-driven)**: broaden the compiler/VM surface only when conformance evidence remains clean.
- **Benchmarks as trends**: add more microbenchmarks with clear intent and interpretability (not performance claims).
- **Tooling consistency**: keep error-code meanings and span policy stable as the language evolves.

## Out-of-scope (explicit)

- Static typing, macros/metaprogramming, concurrency/async.
- Any “performance guarantee” claims.
- A finalized module system spec beyond the currently-implemented behavior.
