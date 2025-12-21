# Thesis Claim

**Claim:**
We show that interpreter↔VM observational equivalence and a stable diagnostics contract can be achieved with explicit, expression-oriented control flow, while preserving scorable evidence under a fixed observation policy and deterministic artifact pipeline.

## Research Questions
- RQ1: Can interpreter and VM executions be made observationally equivalent (value, error, stdout) on a large, seeded program set?
- RQ2: Can diagnostics (error kind, code, span) be made stable and contractually enforced?

## Hypotheses
- H1: Interpreter and VM are observationally equivalent on all programs in the test suite.
- H2: Diagnostics are stable and contractually enforced for all golden cases.

## Success Criteria
- 0 divergences in diff test (see [results/diff_report.md](../results/diff_report.md))
- 100% diagnostics contract pass (see [results/golden_diagnostics.md](../results/golden_diagnostics.md))
- Coverage: all core constructs exercised (see [results/coverage_by_construct.md](../results/coverage_by_construct.md))

## Falsifiers / What Would Invalidate Results
- Any divergence between interpreter and VM on a valid program
- Any diagnostics contract failure (unstable code/span)
- Coverage gaps in core constructs
- Non-deterministic results across runs
