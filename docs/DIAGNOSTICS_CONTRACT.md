# Diagnostics Contract

## Invariants
- Error codes must be stable across versions.
- Error messages may change, but codes and span categories must not.
- Spans must contain the true token location for golden cases.
- Each error code is unique and contractually enforced.
- Diagnostics are deterministic for a given input and commit.
