# Scope control (SuayLang as a research artifact)

SuayLang is intentionally not a “general-purpose production language” project in v0.1. Its purpose is to keep the semantic surface small enough that hypotheses about **explicit control-flow semantics** and **interpreter↔VM equivalence** can be tested and falsified.

## Intentionally out of scope (v0.1)

- **Ecosystem / packages:** no package manager, versioned module ecosystem, or third-party dependency story.
- **Macros / metaprogramming:** no user-defined syntax transformations.
- **Classes / objects / inheritance:** no OOP model or method dispatch.
- **Concurrency / async:** no scheduling model, no nondeterminism from concurrency.
- **FFI / embedding:** no stability guarantees for embedding APIs.
- **Optimization as a goal:** performance is measured, but not claimed as a primary contribution.
- **Implementation-independent standard:** the interpreter is treated as the baseline semantics for v0.1; the VM is evaluated against it.

## Why this narrow scope helps the hypotheses

- Removing large subsystems (modules, concurrency, macros) reduces confounds and makes divergence causes easier to localize.
- A small VM-supported subset makes H2 falsifiable: a divergence is an unambiguous counterexample within the subset.
- Keeping control flow expression-shaped (`dispatch`, `cycle`) keeps H1 tasks focused on the constructs under study.

## Future work (after validation)

- Expand the supported subset and update equivalence evidence as the VM grows.
- Add larger conformance corpora and fuzz generators with broader syntax coverage.
- Add a human-subject study or controlled readability experiment if H1 is pursued beyond structural proxies.
