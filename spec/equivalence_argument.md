# Interpreter ↔ VM equivalence argument (evidence-based)

This document is a proof *sketch* and definition package for the main claim.
It is paired with an artifact pipeline that produces counterexamples when the claim fails.

## Definitions

### Program state

- Interpreter state: `(AST, env, control)`
- VM state: `(code, pc, stack, env)`

### Observation

An observation is a normalized record of:

- termination class (ok / lex / parse / runtime)
- returned value (if ok)
- error code + span policy (if error)

Normalization rules are defined in docs/OBSERVATION_POLICY.md and are part of the claim.

### Observational equivalence

For a set of programs $P$ and an observation function $obs$, we say:

$$\forall p \in P,\; obs(\text{interp}(p)) = obs(\text{vm}(p)).$$

## Invariants required

The compilation and VM execution must preserve:

1) Evaluation order (spec/eval_order.md)
2) Environment/scoping behavior (spec/scopes.md)
3) Error semantics and span policy (spec/errors.md)
4) Determinism (spec/determinism.md)

## Proof sketch outline

1) Define a compilation relation from AST nodes to bytecode fragments.
2) State a simulation relation between interpreter configurations and VM configurations.
3) Prove (by structural induction on expressions) that stepping the interpreter corresponds to stepping the VM until an observation point.
4) Show that error cases produce the same error code and span subject to the diagnostics contract.

## Evidence connection

This is an evidence-based artifact:

- Protocol: `make reproduce-all`
- Counterexample artifact: results/diff_report.md + results/diff_report.json

If a counterexample exists, it refutes the claim for the shipped corpora.
