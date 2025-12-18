# Glossary

- **dispatch**: SuayLang’s expression-shaped pattern match. A scrutinee value is matched top-to-bottom against arms; the first match is selected.
- **cycle**: SuayLang’s pattern-driven loop. A seed state is repeatedly matched against arms; each arm explicitly chooses continue (`↩`) with a new state or finish (`↯`) with a final value.
- **observational equivalence**: Two executions are considered equivalent if they produce the same observable outcome under the repository’s observation policy: termination class, stdout (normalized), value (best-effort structural equality), and error class + coarse (line, column) location.
- **subset (VM-supported subset)**: The explicitly enumerated set of language constructs for which the compiler+VM is expected to match the interpreter. Defined in [docs/spec/supported_subset.md](../spec/supported_subset.md).
- **conformance corpus**: A fixed set of human-readable programs used to check interpreter↔VM equivalence deterministically.
- **differential testing**: Testing strategy that compares two implementations (interpreter vs VM) on the same input programs and treats disagreements as counterexamples.
- **golden diagnostics**: Snapshot-based tests that assert a stable, reviewer-auditable error rendering (message + span caret) for representative error cases.
