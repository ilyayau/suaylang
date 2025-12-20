# Research scope (SuayLang)

This document clarifies the research framing, tooling/product boundaries, and explicit out-of-scope items for SuayLang.

## Research framing
- SuayLang is a research artifact, not a product.
- Tooling (CLI, formatter, VS Code extension) exists to support controlled experiments, reproducibility, and reviewer evaluation.
- All features are justified by their role in the research protocol or evidence generation.

## Tooling vs product scope
- CLI: enables batch testing, deterministic runs, and error reporting for research.
- Formatter: ensures input normalization for corpus generation and reproducibility.
- VS Code extension: provides syntax highlighting and minimal LSP for reviewer accessibility, not as a full IDE.

## Out of scope
- Concurrency, parallelism, async execution
- JIT compilation
- Full type inference or static typing
- Performance as a primary objective (benchmarks are for measurement, not claims)
- Macro/metaprogramming
- A finalized module system spec
- Human usability claims (beyond proxy metrics)

## Threats to validity
- Results may not generalize to larger or more complex languages.
- Diagnostic stability is measured on a fixed corpus; new features may introduce drift.
- Benchmarks are microbenchmarks, not real-world workloads.
- Golden diagnostics only cover a representative subset of errors.

---

**For more, see:**
- [docs/SPEC_V1_SCOPE.md](SPEC_V1_SCOPE.md)
- [docs/RESEARCH_CLAIM.md](RESEARCH_CLAIM.md)
- [docs/METRICS.md](METRICS.md)
