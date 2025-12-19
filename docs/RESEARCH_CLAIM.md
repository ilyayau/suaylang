# Research claim (SuayLang v0.1)

## Problem (2–4 sentences)

Small languages often claim “clear semantics” and “tooling-first design”, but those claims are rarely falsifiable: the reference interpreter, the VM/compiler, and the diagnostics drift over time without a measurable contract.
SuayLang treats backend equivalence and diagnostic stability as first-class research objects and makes them executable: the interpreter is the reference semantics and the bytecode VM is continuously validated against it.

## Hypotheses

### H1 (primary, falsifiable)

For the v0.1 feature subset (Scope), SuayLang’s interpreter and bytecode VM are observationally equivalent on a large, diverse, deterministic program set.

For all generated **valid** programs in the differential test suite (seeds 0–99; size buckets; see protocol), the interpreter and VM agree on:

- termination class (`ok|lex|parse|runtime|internal`)
- normalized stdout
- and, when `ok`, the returned value (best-effort structural equality)

### H2 (optional)

For generated **intentionally-invalid** programs, SuayLang’s diagnostics are stable across backends: error kind (`lex|parse|runtime`) and location (line/column) match.

## Success metrics (quantitative thresholds)

- **Equivalence rate (valid programs)**: 100.0% agreement (0 divergences) for the default full run:
  - seeds = `0..99`
  - `N_valid >= 1000` programs per seed
  - stratified across size buckets `{small, medium, large}`
- **Diagnostic stability (invalid programs)**: ≥ 99.5% agreement on (error kind, line, column) for the same full run.
- **Coverage** (measured on the executed suite):
  - AST node-kind coverage: each AST node kind defined in `suaylang/ast.py` is observed at least once, or explicitly reported as “unreached by generator”.
  - Opcode-kind coverage (static): each opcode kind emitted by the compiler is observed at least once across compiled programs, or explicitly reported as “unreached by generator”.

## Explicit falsification conditions

H1/H2 are falsified if **any** of the following occur in the reproducible full run:

- Any interpreter/VM divergence on valid programs (termination/stdout/value mismatch).
- Any mismatch in diagnostic kind or location (line/column) on invalid programs beyond the 0.5% tolerance.
- Coverage report shows a claimed in-scope construct/opcode is never exercised.

## Scope (feature subset covered by the claim)

Included:

- expressions, blocks, eager left-to-right evaluation (with `&&`/`||` short-circuit)
- binding (`<-`) and mutation (`<~`)
- lambdas and curried calls
- dispatch (`|> { ... }`) pattern matching and variants (`Tag::payload`)
- cycle (`~~ seed |> { ... }`) state-machine loop
- tuples, lists, maps, text, numbers, booleans, unit
- modules via `link` (filesystem modules)

Excluded:

- performance claims (handled separately in [results/benchmarks.md](../results/benchmarks.md))
- human usability claims (handled via proxy protocol in [docs/HUMAN_STUDY.md](HUMAN_STUDY.md))
- proposed future features not implemented in v0.1

## Why this matters academically (6–10 lines)

This artifact operationalizes a semantics/tooling claim as a continuous, executable contract rather than a prose guarantee.
By fixing a reference interpreter as the specification and using large-scale, deterministic differential testing, SuayLang provides a concrete instance of compiler/VM validation under realistic tooling constraints.
The work connects operational semantics concerns (observable behavior, error localization) with practical reproducibility (CI gating, minimized regressions, saved raw reports).
It is designed to be reviewed like a small PL experiment: a falsifiable hypothesis, a protocol, and auditable artifacts.
