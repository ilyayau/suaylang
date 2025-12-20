# Research claim (scorable)

## Problem statement (2–3 sentences)

Small languages often ship multiple execution backends (interpreter, compiler/VM), but “they behave the same” is usually asserted informally.
In practice, semantics and diagnostics drift, and the claim becomes unreviewable.
SuayLang treats backend equivalence and diagnostic stability as research objects and makes them auditable via deterministic, saved artifacts.

## Research question (1 sentence)

Can a small language keep an interpreter and a bytecode VM observationally equivalent under a fixed, explicit Observation Policy, with evidence that is deterministic and reviewer-auditable?

## Falsifiable hypothesis (1–2 sentences)

Under the v1 research scope and Observation Policy in [docs/SPEC_V1_SCOPE.md](SPEC_V1_SCOPE.md), the reference interpreter and the bytecode VM are observationally equivalent on the deterministic differential test suite.
Equivalence is falsified by any reported divergence in the saved reports.

## Method (deterministic; executable)

- **Seeded differential testing**: generate programs deterministically from seeds; run interpreter and VM; compare observations.
  - Implementation: [tools/diff_test/](../tools/diff_test/)
  - Protocol: [docs/EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md)
- **Minimization**: divergences are minimized to a smaller counterexample and saved as regressions.
- **Golden diagnostics**: representative failures are snapshotted to keep error-code mapping and caret-span rendering stable.
  - [tests/test_golden_diagnostics.py](../tests/test_golden_diagnostics.py)
  - [tests/test_golden_error_codes.py](../tests/test_golden_error_codes.py)
- **Coverage reporting**: report observed AST node kinds and emitted opcode kinds on the executed suite.

## Metrics & success criteria (exact)

Primary metrics are read from the saved `results/` artifacts:

- **Divergences**: must be 0 in the published run profile.
  - Report: [results/diff_report.md](../results/diff_report.md) and [results/diff_report.json](../results/diff_report.json)
- **Coverage counts**: report observed AST node kinds and opcode kinds.
  - Report: [results/coverage.md](../results/coverage.md) and [results/coverage.json](../results/coverage.json)
- **Diagnostics stability**: golden snapshot suite must pass.
  - Report (generated): `results/golden_diagnostics.md` and `results/golden_diagnostics.json`

Repro command (single entry point): `make research` (see README).
