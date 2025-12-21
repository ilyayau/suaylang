# Correctness: Observational Equivalence

## Value Equivalence
- Two executions are equivalent if they produce the same value under the observation policy.

## Stdout Equivalence
- Stdout is compared after normalization (whitespace, order if deterministic).

## Error Kind+Span Equivalence
- Errors are equivalent if error code and span category match.

## Side-Effect Scope
- Only stdout is considered; no other side effects are in scope.

## Observation Policy (normative)
- Only value, error (code+span), and stdout are observable.
- Message text and formatting are ignored.
- Non-deterministic output is not allowed.

## Out of Scope
- File I/O, network, or external state
- Non-deterministic behaviors
- Any effects beyond stdout
