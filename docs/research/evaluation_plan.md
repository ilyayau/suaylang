# Evaluation plan (SuayLang research artifacts)

This document describes planned evaluation methodology. It intentionally contains no results.

## Overview

The evaluation is organized into three components:
1) A rubric-based micro-evaluation of control-flow design.
2) Interpreter vs VM conformance evidence via differential testing.
3) Micro-benchmarks measuring relative performance of interpreter vs VM.

All evaluation artifacts are designed to be:
- reproducible from a fresh checkout,
- conservative about claims,
- explicit about scope and limitations.

## 1) Micro-evaluation of control flow (rubric-based)

Goal: produce measured, transparent descriptive comparisons on small tasks.

Baseline:
- Python (primary baseline, due to reviewer familiarity).

Tasks (fixed set):
- branching-heavy logic
- iterative state evolution (state machine)
- small interpreter-like logic

Metrics:
- LOC (non-empty, non-comment)
- control-construct counts
- local reasoning steps rubric (pre-declared)

Outputs:
- a small comparison table
- an explicit discussion of limitations (no human-subject claims)

## 2) Interpreter vs VM conformance (hard evidence)

Goal: provide evidence that the VM matches the reference interpreter on a documented subset.

Definition:
- observational equivalence is defined in terms of termination kind, stdout, and location/spans for errors.

Scope:
- conformance is claimed only for the subset supported by the compiler/VM.

Planned evidence:
- a shared test corpus of `.suay` programs executed by both implementations
- a differential runner that compares observations
- a bounded generative component (e.g., random AST/program generation within a supported subset)

Non-goals:
- matching error message text exactly (unless in strict mode)
- claiming equivalence outside the documented subset

## 3) Micro-benchmarks (relative; no speed race)

Goal: justify the existence of the VM as an engineering artifact by measuring relative performance on relevant micro-programs.

Principles:
- relative comparison only (VM vs interpreter)
- avoid “fastest language” claims
- control stdout/stderr to avoid I/O dominating timings

Benchmark categories:
- dispatch-heavy programs
- cycle-heavy state machines
- function-call-heavy programs
- mixed workloads

Outputs:
- benchmark code (programs)
- a small timing table (median/min/max)
- conservative interpretation (what is and is not supported by the data)
