# SuayLang: Draft Paper (Working Draft)

Status: working draft in-repo. No external preprint upload is claimed.

## Abstract

SuayLang is a research language designed to study observational equivalence between two independent executions: a reference interpreter and a bytecode VM. The artifact contributes a committee-auditable packaging style: an explicit observation policy, a claim→artifact→command mapping, and integrity metadata (hashes) over generated evidence.

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

## 5. Limitations

- docs/LIMITATIONS.md

## 6. Threats to validity

- docs/THREATS_TO_VALIDITY.md

## 7. Related work

- README.md (Related work links)
- citations.bib

## 8. Reproducibility

- docs/REPRODUCIBILITY.md
- results/independent_reproduction/receipt_template.md
