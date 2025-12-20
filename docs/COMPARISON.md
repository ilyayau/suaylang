# Comparison: SuayLang vs Baselines

## Table: SuayLang vs Rust vs Python vs Lisp/ML-family

| Criterion                    | SuayLang         | Rust            | Python          | Lisp/ML-family   |
|------------------------------|------------------|-----------------|-----------------|------------------|
| Control flow composability   | Expression-based, pattern match, cycle | Statement + match | Statement, no match | Expression, match (ML) |
| Error reporting contract     | Stable error codes, spans, golden tests, artifact-backed | Error types, messages | Exceptions, messages | Exceptions, messages  |
| Interpreter↔VM equivalence   | Differential testing, artifact-backed, results saved | No explicit contract | No explicit contract | No explicit contract   |
| Tooling hooks                | CLI, formatter, VSCode, artifact gen, deterministic runner | Cargo, rustfmt, LSP | CLI, pip, LSP       | REPL, LSP, formatters  |
| Semantics clarity            | Formalized, documented, artifact-linked, minimal model | Reference, docs     | Reference, docs     | Reference, docs        |
| Coverage reporting           | AST/opcode coverage, results artifacts | Test coverage    | Test coverage      | Test coverage          |
| Baseline comparison          | Naive interpreter, diagnostics contract (planned) | N/A | N/A | N/A |


## Where SuayLang differs
- Backend equivalence and diagnostics are scorable, artifact-backed, and reviewer-auditable.
- Observation policy and error model are explicit and enforced by tests.
- Results and metrics are saved as artifacts, not just logs.
- Deterministic runner (`make research`) regenerates all results and environment metadata.
- Baseline comparisons are planned and will be included in results/baseline.md.


## Related Work (concept-level)
- Differential testing of compilers/VMs (McKeeman, Yang et al.)
- Conformance suites for language validation (Wasm, JavaScript)
- Operational semantics for language design (Plotkin, Kahn)
- Pattern matching and expression-oriented control flow (ML, Haskell, Rust)
- Structured diagnostics contracts (Rust error codes, Elm diagnostics)
- Golden tests for diagnostics stability (Elm, Rust, SuayLang)
- Artifact-based reproducibility in PL research (PLDI, OOPSLA artifact tracks)
- Coverage-driven program generation (QuickCheck, property-based testing)
- Regression minimization and corpus growth (C-Reduce, SuayLang minimizer)
- Tooling for reviewer-facing evidence (artifact evaluation, reproducibility badges)

---

**See also:**
- [docs/RESEARCH.md](RESEARCH.md)
- [docs/SEMANTICS.md](SEMANTICS.md)
- [results/README.md](../results/README.md)
