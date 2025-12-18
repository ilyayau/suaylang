# Executive Summary (≈ 1 page)

## Problem statement

When a language implementation grows from a reference interpreter into a compiler+VM, semantic drift becomes a primary research and engineering risk: two execution paths can disagree in user-visible ways. The core problem is to make such disagreement **falsifiable** and **automatically detectable** on a clearly defined subset, without requiring a full formalization.

## Research questions

- **RQ1:** Can an interpreter and bytecode VM be made observationally equivalent on an explicitly defined subset, with equivalence validated automatically?
- **RQ2 (optional):** Do expression-shaped control-flow constructs (`dispatch`, `cycle`) reduce structural proxies of local reasoning complexity relative to statement-shaped baselines on selected tasks?

## Hypotheses (falsifiable)

- **H2 (required):** Interpreter and bytecode VM can be made observationally equivalent on a defined subset, and equivalence can be validated automatically.
- **H1 (optional, proxy-based):** Expression-based explicit control flow reduces local reasoning complexity compared to statement-based control flow on selected tasks.

## Methods (what is measured)

- **Observational equivalence (H2):** compare interpreter vs VM observations for (termination class, stdout, value, error class + coarse location) on:
  - a fixed, versioned conformance corpus, and
  - seeded differential fuzz generation.
- **Readability proxies (H1):** token count, approximate AST depth, and branch-point counts on 5 paired tasks (SuayLang vs Python).

## Snapshot results (numbers)

- Conformance corpus: `M = 30` programs, divergences `= 0`.
- Differential fuzz: seed `= 0`, `N = 1000`, divergences `= 0`.
- Supported subset size: `X = 14` expression-level constructs listed in the subset spec.

## Why this matters academically

This artifact is positioned as reproducible evidence in the intersection of:

- PL implementation validation (interpreter↔VM equivalence evidence)
- differential testing / fuzzing applied to language implementations
- explicit operational-style control flow as a design point enabling testable semantics

## Limitations (explicit)

- Equivalence is claimed only on the VM-supported subset; interpreter-only features (e.g., modules) are excluded.
- Fuzz generation is bounded and template-based; it is not an unbiased sample of all programs.
- H1 evidence is proxy-based and not a human-subject comprehension study.

## Commission flags: why Japan should fund this (specific, non-marketing)

- The work is **reproducible**: deterministic seeds, fixed corpora, and artifact-producing CI enable independent verification.
- It is strong **training value** for PL tooling/semantics: students can study a complete pipeline (lexer→parser→AST→interp→compiler→VM→diagnostics→validation).
- It is a plausible **publication trajectory**: the methodology and results are scoped to be auditable, with clear next steps for stronger evaluation.
