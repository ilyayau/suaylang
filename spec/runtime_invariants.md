# Runtime invariants

These invariants are intended to be testable and are relied upon by the equivalence claim.

1) **Value determinism:** evaluation produces the same value given the same inputs.
2) **Environment chain well-formedness:** every env has an optional parent; lookups terminate.
3) **Stack safety (VM):** stack underflow is impossible in well-compiled code; if it occurs, it is a bug.
4) **Program counter safety (VM):** pc always references a valid instruction index in the current code.
5) **Closure capture correctness:** captured environment matches lambda definition site.

Test connection:
- Violations are expected to manifest as counterexamples in results/diff_report.* when running `make reproduce-all`.
