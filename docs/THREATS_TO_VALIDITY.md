# Threats to Validity

## Internal Validity
- **Scenario:** Shared code or test harness bug masks backend divergence.
- **Mitigation:** Mutation/injection tests, code review, independent baseline.
- **Remaining Risk:** Uncaught shared logic errors.

## External Validity
- **Scenario:** Test suite does not cover all real-world program patterns.
- **Mitigation:** Multi-seed generator, manual stress cases, coverage reporting.
- **Remaining Risk:** Unseen edge cases in the wild.

## Construct Validity
- **Scenario:** Observation policy or equivalence definition omits relevant behaviors.
- **Mitigation:** Formalized policy, explicit out-of-scope list, reviewer feedback.
- **Remaining Risk:** Reviewer disagreement on what should be observed.
