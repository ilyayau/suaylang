# Related work (categorized)

This section is intentionally scoped to the methodology-level contributions of this artifact.
Bibliography: docs/refs.bib.

## Differential testing / compiler validation

- Example class: randomized compiler testing / differential execution (e.g., Csmith). (yang2011csmith)
- Why it matters here: motivates “two independent executions” as a practical validation strategy.
- Limitation of the class: differential testing can miss shared-oracle bugs and can under-sample semantically hard cases.

## Property-based testing

- Example class: property-based testing with generation + shrinking (e.g., QuickCheck). (claessen2000quickcheck)
- Why it matters here: deterministic seeds and minimized counterexamples make failures reproducible.
- Limitation of the class: generator bias can produce false confidence; properties can be under-specified.

## Mutation testing

- Example class: mutation testing to assess adequacy. (jia2011mutation)
- Why it matters here: helps bound the “shared-oracle” threat by testing whether suites actually detect injected bugs.
- Limitation of the class: mutation score can be expensive and can overfit to mutation operators.

## Artifact evaluation and reproducibility norms

- SIGPLAN AE guidance motivates committee-first packaging.
- Reproducible builds culture motivates integrity metadata and explicit environment disclosure. (sigplan-ae, reproducible-builds)

Limitation of the class:
- Passing reproducibility checks does not imply correctness; it only implies the protocol is executable and stable.

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

## Where ours differs (one sentence)

SuayLang differs by treating equivalence as a falsifiable, artifact-indexed claim (policy → protocol → generated counterexamples) rather than an informal statement about two implementations.

