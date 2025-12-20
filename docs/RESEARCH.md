# Research framing (SuayLang)

## Problem statement
Most small languages claim “clear semantics” and “tooling-first design,” but backend equivalence and diagnostics stability are rarely falsifiable or reviewer-auditable.

## Research Questions
- **RQ1:** Can interpreter and VM executions be made observationally equivalent under a fixed, explicit observation policy?
- **RQ2:** Can diagnostics (error kind, code, span) be made stable and contractually enforced across backends?
- **RQ3:** Can all claims be made reviewer-auditable via deterministic, saved artifacts?

## Hypotheses (falsifiable)
- **H1:** Interpreter and VM are observationally equivalent (termination, value, stdout) on a large, seeded program set. Falsified by any divergence in results/diff_report.md.
- **H2:** Diagnostics (error kind, code, span) are stable and contractually enforced via golden tests. Falsified by any mismatch in golden diagnostics.

## Success metrics
- Divergences: 0 in CI profile (see results/diff_report.md)
- Diagnostic stability: 100% in golden diagnostics (see results/golden_diagnostics.md)
- Coverage: ≥24 AST node kinds, ≥20 opcode kinds (see results/coverage.md)
- Benchmarks: 6 programs, median/p90 timings (see results/benchmarks.md)

## Threats to validity
- Results may not generalize to larger or more complex languages.
- Diagnostic stability is measured on a fixed corpus; new features may introduce drift.
- Benchmarks are microbenchmarks, not real-world workloads.
- Golden diagnostics only cover a representative subset of errors.

## Scope / Non-goals
- Out of scope: concurrency, JIT, full type system, macro/metaprogramming, finalized module system, performance as a primary objective, human usability claims.

---

**See also:**
- [docs/SEMANTICS.md](SEMANTICS.md)
- [docs/COMPARISON.md](COMPARISON.md)
- [docs/ROADMAP.md](ROADMAP.md)
- [results/README.md](../results/README.md)
