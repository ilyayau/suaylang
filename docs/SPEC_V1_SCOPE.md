# v1 Scope (Scorable) — Semantics + Observation Policy

This document defines a **scorable** v1 research scope: what SuayLang claims to preserve across the reference interpreter and the bytecode VM, and **exactly what is observed** to validate that claim.

This is intentionally narrower than “everything in the language reference”. The goal is to be reviewable and falsifiable.

See also:
- Protocol: [docs/EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md)
- Conformance definition: [docs/CONFORMANCE.md](CONFORMANCE.md)

## 1) v1 Scope (what is guaranteed)

Within this scope, SuayLang guarantees:

1) **Deterministic evaluation** (single-threaded) for the same source text.
2) **Observational equivalence** between:
   - the reference interpreter, and
   - the bytecode compiler+VM,
   under the Observation Policy below.

### In-scope constructs

The equivalence claim applies to programs using the implemented core:

- Expressions and strict left-to-right evaluation.
- Literals and values: unit, bool, int/dec, text, tuple, list, map, variants.
- Binding and lexical scoping via blocks.
- Lambdas + function application (curried calls).
- Pattern matching via `dispatch` and state-machine loops via `cycle`.
- A small, stable builtin surface (documented in [docs/STDLIB_REFERENCE.md](STDLIB_REFERENCE.md)).
- Module loading via the current `link` mechanism (when exercised by the benchmark/corpus), without claiming a finalized module-system spec.

### Determinism expectations

Within scope, a run is expected to be deterministic with respect to:

- termination class,
- printed output,
- and the returned value (when comparable under the policy).

## 2) Observation Policy (what outputs are compared)

The differential test harness validates equivalence using a structured “observation” emitted by each backend.

Implementation reference: [tools/diff_test/comparator.py](../tools/diff_test/comparator.py).

### 2.1 Compared fields

Two runs are considered equivalent iff all of the following match:

1) **Termination class**: one of `ok|lex|parse|runtime|internal`.
2) **Normalized stdout**: newline normalization only (`\r\n → \n`).
3) If termination is `ok`: **returned value representation** (`value_repr`), with an explicit exception for opaque runtime values.
4) If termination is an error (`lex|parse|runtime|internal`): **error type** and **primary location**:
   - `error_type` (coarse kind)
   - `(line, column)` (1-based)

### 2.2 Allowed to differ (recorded, not compared)

- **stderr** may differ; it is captured for debugging but not used for equivalence.
- **Error message text** may differ in the differential test harness.

### 2.3 Opaque ok-values

When termination is `ok`, returned values are compared by string representation.
However, certain runtime values are treated as intentionally opaque across backends (interpreter/VM have different internal representations):

- closures,
- builtins.

If *both* backends return an opaque value (as detected by the comparator), the run is treated as equivalent.

### 2.4 Diagnostics “shape” policy (separate from diff-test)

To keep diagnostics reviewer-stable, SuayLang also maintains **golden snapshots** for representative failures:

- unprefixed diagnostic rendering (caret spans, message skeleton)
- code-prefixed diagnostics (stable error-code mapping)

Implementation:
- [tests/test_golden_diagnostics.py](../tests/test_golden_diagnostics.py)
- [tests/test_golden_error_codes.py](../tests/test_golden_error_codes.py)

The research runner generates a machine-readable summary under `results/`.

## 3) Non-goals (explicitly excluded)

These are explicitly *not* claimed by v1 scope:

- Performance claims (benchmarks are reported as measurement artifacts, not guarantees).
- Bytecode format stability.
- A fully specified module system beyond the currently-implemented behavior.
- Concurrency, async, macros/metaprogramming, static typing.
- Exact error message text stability across the full input space (goldens cover a small representative set).
- Any “human usability” outcome beyond the separate proxy study artifacts.

## 4) What would falsify the claim

The v1 scope is falsified by any of the following in a reproducible run:

1) Any interpreter↔VM divergence under the Observation Policy on valid programs.
2) Any mismatch in (error type, line, column) under the Observation Policy on invalid programs beyond the configured tolerance (when a tolerance is claimed).
3) Any failure of the golden diagnostics snapshot suite.

The saved evidence for reviewers is the set of reports under `results/` (see README “Results at a glance”).
