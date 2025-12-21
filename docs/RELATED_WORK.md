# Related Work

- **Differential Testing:** Used in compiler validation (e.g., Csmith). Misses: often lacks formal observation policy. SuayLang: adds explicit, auditable equivalence.
- **QuickCheck/Property-Based Testing:** Widely used for randomized testing. Misses: not always deterministic or reproducible. SuayLang: fixes seeds, records all outputs.
- **Conformance Suites:** (e.g., ECMAScript). Misses: rarely enforce backend equivalence. SuayLang: makes equivalence a first-class, testable property.
- **Operational Semantics (Plotkin/Kahn):** Foundation for language definition. Misses: not always executable or linked to artifact evidence. SuayLang: formal core is executable and evidenced.
- **Golden Diagnostics:** Used in Rust, OCaml. Misses: not always contractually enforced. SuayLang: diagnostics contract is explicit and tested.
- **Mutation/Injection Testing:** Used for robustness. SuayLang: applies to backend equivalence and diagnostics.
- **Artifact Evaluation Protocols:** (e.g., SIGPLAN AE). SuayLang: follows reproducibility, evidence, and auditability standards.

