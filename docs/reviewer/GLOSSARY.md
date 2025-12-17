# Glossary

- **dispatch:** SuayLang’s pattern-match expression (`value ▷ ⟪ ▷ pat ⇒ expr ... ⟫`). The first matching arm is selected.
- **cycle:** SuayLang’s pattern-driven loop expression (`⟲ seed ▷ ⟪ ... ⟫`) where each arm returns either **continue** (`↩`) with a new state or **finish** (`↯`) with a final value.
- **observational equivalence:** Two executions are treated as equivalent if they have the same observable outcome under the project’s observation policy: termination class, normalized stdout, value (best-effort structural equality), and for errors: error class and coarse (line, column).
- **subset (VM-supported subset):** The set of language constructs for which the VM compiler supports compilation and the equivalence claim is made. Defined in [docs/spec/supported_subset.md](../spec/supported_subset.md).
- **conformance corpus:** A fixed set of human-readable programs used to compare interpreter vs VM outcomes deterministically.
- **differential testing:** Testing technique that runs two implementations on the same inputs and flags any behavioral disagreement as a counterexample.
- **fuzzing (seeded, deterministic):** Program generation driven by a fixed RNG seed so runs can be replicated exactly.
- **golden diagnostics:** Snapshot-based tests that assert stable diagnostic text/spans for a fixed set of error-triggering programs.
