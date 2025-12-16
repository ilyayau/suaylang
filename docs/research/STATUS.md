# Research artifact status (SuayLang)

This folder contains research-oriented documentation and scaffolding for formal evaluation of SuayLang, without changing language semantics or existing behavior.

## Current project state

SuayLang is an expression-oriented language with explicit, pattern-driven control flow:
- `dispatch` (`▷ … ⇒ …`) for branching
- `cycle` (`⟲ … ↩ … / ↯ …`) for state-machine style iteration

The repository contains two execution paths:
- **Reference interpreter**: the semantic baseline for v0.1 programs.
- **Bytecode compiler + VM**: a second implementation intended for engineering exploration and comparative evaluation on a supported subset.

## Baseline semantics

For research and evaluation purposes, **the interpreter defines baseline semantics** for SuayLang v0.1.

Authoritative definitions:
- Language contract: docs/LANGUAGE_CONTRACT_v0.1.md
- Grammar reference: docs/GRAMMAR.md

Evaluation and tooling in this folder must not modify:
- interpreter logic or behavior
- VM semantics
- public APIs

## VM scope (in-scope vs out-of-scope)

### In-scope (for conformance and benchmarks)

The VM is considered in-scope only for constructs that are:
1) part of the v0.1 contract, and
2) implemented by the compiler/VM without falling back to unimplemented behavior.

In practice, this includes the core expression forms supported by the compiler (e.g., literals, bindings, function application, and the `dispatch`/`cycle` forms where implemented).

### Out-of-scope (explicit)

The following are out-of-scope for interpreter↔VM equivalence claims unless explicitly added to the conformance subset definition:
- Module loading via `link` (the interpreter has module loading support; the VM does not implement modules)
- Any AST node not supported by the compiler (treated as “not evaluated,” not “equivalent”)
- Exact wording of error messages and stack trace formatting (the v0.1 contract treats these as unstable details)

## Known limitations (research-relevant)

- **No human-subject study**: the planned evaluation is rubric-based and descriptive.
- **Unicode confound**: Unicode-heavy syntax affects accessibility and may confound readability claims.
- **Subset conformance**: conformance can only be claimed for a documented subset supported by the VM.
- **I/O behavior**: programs may perform I/O (`say`, `hear`); conformance claims must either restrict I/O or control it.
