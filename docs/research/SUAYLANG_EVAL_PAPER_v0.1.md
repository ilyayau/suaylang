# SuayLang v0.1 — Research Artifact for Micro-Evaluation

*This document is intended to be converted to PDF for academic review (4–8 pages).*  
*It is intentionally conservative and focuses on evidence, not promotion.*

## Abstract

SuayLang is an expression-oriented language in which control flow is represented as expressions via pattern-driven operators: `dispatch` (branching) and `cycle` (state-machine iteration). The language is implemented by a reference interpreter and a bytecode compiler + VM. This artifact provides a micro-evaluation intended for skeptical review: (1) an explicit hypothesis about composability and local reasoning, (2) a rubric-based comparison against a baseline language (Python) on fixed tasks, (3) hard conformance evidence via differential testing between interpreter and VM on a defined subset, (4) micro-benchmarks measuring relative (not absolute) performance of interpreter vs VM on control-flow-heavy programs, and (5) a discussion of Unicode-heavy syntax as a research variable.

## 1. Motivation

Most mainstream languages represent branching and looping primarily as statements, which can create non-local reasoning obligations (implicit control destinations, implicit loop state transitions, and mutation-driven state). SuayLang explores a different point in the design space: control flow as expressions, with explicit state evolution and pattern matching.

The goal is not to claim universal superiority; it is to provide a precise artifact that allows reviewers to evaluate whether explicit, pattern-driven control flow supports composability and predictable semantics.

## 2. Research hypothesis

See docs/research/HYPOTHESIS.md.

Primary hypothesis (H1): expression-based, pattern-driven control flow improves composability and local reasoning.

## 3. Language design (v0.1)

SuayLang v0.1 is defined by:
- a language contract: docs/LANGUAGE_CONTRACT_v0.1.md
- a grammar reference: docs/GRAMMAR.md

The core control-flow operators are:
- `dispatch`: pattern-based branching as an expression
- `cycle`: pattern-based iteration as an explicit state machine (`↩` continue / `↯` finish)

Unicode syntax is a deliberate design variable (§7).

## 4. Implementation overview

SuayLang includes:
- A reference interpreter (semantic authority for v0.1).
- A bytecode compiler + stack VM for a supported subset.

The bytecode format is an implementation detail; the language-level semantics are described by the contract.

## 5. Micro-evaluation methodology

See docs/research/MICRO_EVAL.md.

We compare SuayLang against Python using fixed tasks and measured descriptive metrics:
- M1: LOC
- M2: control construct count
- M3: local reasoning steps (explicit rubric; reported conservatively)

This is not a user study; it is intended to be reproducible and honest about limitations.

## 6. Conformance evidence (interpreter vs VM)

See docs/research/CONFORMANCE.md.

We define observational equivalence for a supported subset and provide two forms of evidence:
- A shared corpus of programs executed by both implementations.
- A bounded generative differential test searching for divergences.

This yields hard evidence that the VM matches interpreter behavior on the evaluated subset.

## 7. Micro-benchmarks (relative, not absolute)

See docs/research/BENCHMARKS_v0.1.md.

We measure relative timing of interpreter vs VM on:
- dispatch-heavy programs
- cycle-heavy state machines
- function-call-heavy programs

We do not claim “fastest language” outcomes; results are interpreted as support for the VM’s existence as an engineering artifact.

## 8. Unicode syntax as a research variable

See docs/research/UNICODE_VARIABLE.md.

Unicode-heavy syntax can improve symbol-level disambiguation but introduces accessibility and tooling costs; these costs are part of the research artifact and should be considered in any readability discussion.

## 9. Limitations and future work

- No human-subject evaluation; comprehension claims are not made.
- VM conformance is only claimed for a documented subset.
- Unicode confounds readability; a future controlled experiment could compare Unicode vs ASCII surface forms while holding semantics fixed.

## 10. Reproducibility (15-minute reviewer path)

From a fresh checkout:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"

pytest -q
python scripts/smoke.py
python scripts/conformance.py
python scripts/bench_micro.py
```

Claims → evidence map:
- docs/research/CLAIMS_EVIDENCE_CHECKLIST.md
