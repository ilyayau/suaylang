# SuayLang: Draft Paper (Working Draft)

Status: working draft in-repo. No external preprint upload is claimed.

## Abstract

SuayLang is a research language designed to study observational equivalence between two independent executions: a reference interpreter and a bytecode VM. The artifact contributes a committee-auditable packaging style: an explicit observation policy, a claim→artifact→command mapping, and integrity metadata (hashes) over generated evidence.

**Keywords:** programming languages, artifact evaluation, reproducibility, differential testing, virtual machines.

## Research question (1 sentence)

Can a reference interpreter and a bytecode VM be made observationally equivalent under a fixed observation policy, and evaluated via a deterministic, artifact-driven protocol?

## Hypothesis (falsifiable)

For the shipped corpora and supported subset, interpreter and VM observations are equivalent under docs/OBSERVATION_POLICY.md.

**Falsifiable criteria:** any disagreement on termination class, normalized stdout, returned value (for `ok`), or error kind/span (line/column) falsifies the hypothesis for that case.

## Novelty (explicit vs prior work)

Novelty is methodological: this artifact makes the equivalence claim committee-auditable via an explicit observation policy, an evidence map, and integrity metadata.
See docs/RELATED_WORK.md.

## Contributions

- **C1:** Deterministic equivalence evaluation protocol with a single entrypoint (`make reproduce-all`).
- **C2:** Observation and diagnostics contracts enabling stable comparisons.
- **C3:** Artifact-driven evidence packaging (results index + hashes) designed for committee review.

## 1. Introduction

### Problem

Backend equivalence claims in language tooling are often communicated narratively or via ad-hoc tests, making committee review and independent reproduction difficult.

### Contribution

We package equivalence evaluation as an artifact whose evidence is file-based, reproducible, and directly mapped to claims.

## 2. Method

### Observation policy

- Normative definition: docs/OBSERVATION_POLICY.md
- What is observed: value / error (code + span categories) / stdout
- What is excluded: defined exclusions in the policy

### Protocol

Canonical reproduction command:

```sh
make reproduce-all
```

Artifacts are indexed under results/README.md.

### What fails if the hypothesis is wrong

- CI / tests should fail.
- A counterexample divergence should be produced by conformance or diff-test tooling and recorded for regression.

See docs/RESEARCH_FRAMING.md.

## 3. Implementation

- Reference interpreter: suaylang/interpreter.py
- Bytecode compiler: suaylang/compiler.py
- Bytecode VM: suaylang/vm.py
- Bytecode model: docs/BYTECODE.md

## 4. Evaluation

This draft avoids hard-coding numeric results.

Read concrete values from generated artifacts:

- results/baseline.md and results/baseline_raw.json
- results/manifest.json and results/hashes.txt
- docs/plots/microbench_relative.png

Evaluation protocol (standalone): docs/EVALUATION_PROTOCOL.md.

## 5. Limitations

- docs/LIMITATIONS.md

## 5.1 Explicit assumptions

- Linux + Python 3.12.x is the primary supported evaluation environment (CI pins 3.12).
- Functional observations must be deterministic for a fixed commit and input.
- Timing is expected to vary across machines.

## 6. Threats to validity

- docs/THREATS_TO_VALIDITY.md

## 6.1 Ethics statement

- docs/ETHICS.md

## 7. Related work

- docs/RELATED_WORK.md
- docs/refs.bib and docs/citations.bib

## 8. Negative results

This repository does not claim negative results in the narrative.
If divergences are found, they are treated as falsification signals and recorded as counterexamples in the evaluation outputs.

## 8. Reproducibility

- docs/REPRODUCIBILITY.md
- results/independent_reproduction/receipt_template.md

ACM-style checklist: docs/ACM_REPRODUCIBILITY_CHECKLIST.md.

## Citation policy and how to cite

- Citation policy: docs/CITATION_POLICY.md
- How to cite: CITATION.cff and docs/citations.bib

## Publication targets

See docs/PUBLICATION_PLAN.md.

## Glossary and notation

- Glossary: docs/GLOSSARY.md
- Notation: docs/NOTATION.md
