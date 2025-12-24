# Related Work (Skeleton)

This file is a structured placeholder for a citation-ready “Related Work” section.
Populate bibliographic entries in docs/refs.bib and replace the placeholders below.

## Differential testing / compiler validation

- Random program generation for compiler testing (placeholder: [csmith]).
- Differential testing as a validation technique (placeholder: [differential-testing-survey]).

## Property-based testing

- QuickCheck-style generative testing (placeholder: [quickcheck]).

## Conformance suites and reference tests

- Conformance suite methodology (placeholder: [conformance-suites]).

## Operational / denotational semantics

- Operational semantics foundations (placeholder: [plotkin-operational-semantics]).
- Denotational semantics foundations (placeholder: [scott-strachey]).

## Diagnostics contracts / golden tests

- Golden testing for diagnostics in compilers/tools (placeholder: [rustc-diagnostics], [ocaml-diagnostics]).

## Mutation testing

- Mutation testing principles and practice (placeholder: [mutation-testing]).

## Artifact evaluation and reproducibility norms

- SIGPLAN-style artifact evaluation guidelines (placeholder: [sigplan-ae]).

## Positioning note (what this artifact adds)

SuayLang’s contribution is not a new testing primitive; it is packaging the validation story as:

- an explicit observation policy (what is compared, what is excluded),
- a claim→artifact→command mapping, and
- integrity metadata (hashes) for committee review.

