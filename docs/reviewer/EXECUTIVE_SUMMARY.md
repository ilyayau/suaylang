# Executive summary (committee-facing, ~1 page)

## Problem statement

Many language artifacts ship two execution paths (a reference interpreter and an optimized compiler/VM). Without systematic evidence, the two backends can diverge: the same program may yield different values, errors, or observable I/O. This is a reproducibility and correctness problem for research prototypes and for educational interpreters that evolve into VMs.

## Research questions

- **RQ1 (Equivalence):** Can a reference interpreter and a bytecode VM for the same language be kept **observationally equivalent** on a clearly defined subset, and can this be validated automatically?
- **RQ2 (Design proxy):** Do expression-shaped explicit control-flow constructs (`dispatch`, `cycle`) reduce *structural* proxies for local reasoning complexity relative to a statement-based baseline on selected tasks?

## Hypotheses (falsifiable)

- **H2 (required):** Interpreter and bytecode VM can be made observationally equivalent on a defined subset, and equivalence can be validated automatically.
- **H1 (optional, proxy-based):** Expression-based explicit control flow reduces local reasoning complexity compared to statement-based control flow on selected tasks.

Falsification criteria are stated in [docs/research/RESEARCH_CORE.md](../research/RESEARCH_CORE.md).

## Methods (what is measured)

- **Conformance corpus:** fixed `.suay` programs run on interpreter and VM; compare observable outcomes (termination class, stdout, value, error class + location).
- **Seeded differential fuzzing:** deterministic generator produces bounded programs; interpreter and VM observations are compared; raw JSONL logs are saved.
- **Structural proxy metrics (H1):** token count, approximate AST depth, and branch-point count on a fixed 5-task suite comparing SuayLang vs Python.

## Snapshot results (reproducible numbers)

These are the current recorded numbers for v0.1.0 (rerunnable; timings are machine-dependent):

- **Conformance:** fixed corpora total **M = 10** files (4 in `tests/corpus/conformance/` + 6 in `evaluation/tasks/`), **divergences = 0**.
- **Differential fuzz:** seed=0, **N = 1000**, **divergences = 0**.
- **Supported subset:** **X = 14** expression-construct categories (see [docs/spec/supported_subset.md](../spec/supported_subset.md)).

## Why this matters academically

- **PL semantics:** makes semantic drift between two operational implementations falsifiable via counterexamples.
- **PL tooling/testing:** demonstrates a small, repeatable evaluation pipeline that produces artifacts (corpora, seeds, raw logs) suitable for audit.
- **VM validation:** treats the VM as an implementation subject to evidence rather than as an assumed improvement.

## Limitations (explicit)

- Equivalence is claimed only on a **defined VM-supported subset** (no module loading via `link`).
- Fuzzing is bounded and template-driven; it is evidence, not a proof.
- H1 is evaluated via structural proxies, not via human-subject studies.

## Why Japan should fund this (specific, non-marketing)

- Produces a **reproducible open research artifact** in PL semantics/tooling with a low barrier to audit (single-command pipelines).
- Serves as a **training-grade implementation** for semantics, testing, and VM validation that can be used in courses and labs.
- Has a clear **publication trajectory** (workshop-level validation/testing venues) with concrete next steps.
- Collaboration-ready: small scope, explicit subset, deterministic seeds, and raw output logs make external replication feasible.
