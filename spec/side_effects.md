# Side effects

This artifact intentionally minimizes side effects to support reproducibility.

## Defined effects

- environment mutation via `⇐`
- output via stdout/stderr (not part of semantic equivalence unless explicitly observed)

## Not part of semantics

- wall-clock time
- filesystem state
- network state

Observation and normalization are defined in docs/OBSERVATION_POLICY.md.
