# Related work (categorized)

This section is intentionally scoped to the methodology-level contributions of this artifact.
Bibliography: docs/refs.bib.

## Differential testing / compiler validation

- Csmith established large-scale randomized compiler testing via differential behavior across compilers and options. It motivates “two independent executions” as a practical validation strategy. (yang2011csmith)

## Property-based testing

- QuickCheck popularized generative testing with shrinking counterexamples. The SuayLang fuzz/diff-test tooling follows the same spirit: deterministic seeds + minimized regressions. (claessen2000quickcheck)

## Mutation testing

- Mutation testing literature frames systematic fault injection as a way to evaluate test adequacy; we cite it as a future strengthening direction for this artifact’s adequacy story. (jia2011mutation)

## Artifact evaluation and reproducibility norms

- SIGPLAN AE guidance motivates committee-first packaging.
- Reproducible builds culture motivates integrity metadata and explicit environment disclosure. (sigplan-ae, reproducible-builds)

## Novelty / positioning (explicit)

SuayLang’s novelty is *not* a new testing primitive.
The novelty is an **academic packaging pattern** for backend-equivalence claims:

- an explicit observation policy (what counts as “equivalent”),
- a claim → evidence → artifact mapping (what files support which claims), and
- integrity metadata (hashes) designed for committee review and independent reproduction.

## Ours vs prior art (methodology table)

| Approach | Typical goal | Typical output | What SuayLang adds |
|---|---|---|---|
| Randomized compiler testing (e.g., Csmith) | Find compiler miscompilations | Bug reports + minimized C programs | A committee-first evidence map + integrity metadata for the whole evaluation pipeline |
| Property-based testing (e.g., QuickCheck) | Validate properties via generated inputs | Test suites + shrunk counterexamples | A language-level observation policy + interpreter/VM equivalence comparator as an explicit protocol |
| Mutation testing (surveyed) | Measure test adequacy | Mutation score | (Planned) adequacy strengthening; not claimed as complete in v0.1 |
| Artifact-evaluation norms | Standardize reproducibility | Checklists + badges | Concretely integrated into Make targets + results/ artifact index |

