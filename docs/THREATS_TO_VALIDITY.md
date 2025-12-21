# Threats to Validity

## Internal Validity
- **What:** Shared code or test harness bug masks backend divergence.
- **Why:** False negatives possible if logic is duplicated.
- **Mitigation:** Mutation/injection tests, code review, independent baseline.
- **Residual risk:** Uncaught shared logic errors.

## Construct Validity
- **What:** Observation policy or equivalence definition omits relevant behaviors.
- **Why:** May miss real divergences.
- **Mitigation:** Formalized policy, explicit out-of-scope list, reviewer feedback.
- **Residual risk:** Reviewer disagreement on what should be observed.

## External Validity
- **What:** Test suite does not cover all real-world program patterns.
- **Why:** Generator bias, missing edge cases.
- **Mitigation:** Multi-seed generator, manual stress cases, coverage reporting.
- **Residual risk:** Unseen edge cases in the wild.

## Reproducibility Risks
- **What:** Results not reproducible on other OS/Python versions.
- **Why:** Environment drift, dependency changes.
- **Mitigation:** Pinned deps, environment capture, CI artifacts.
- **Residual risk:** Unreproducible on non-Linux or future Python.
