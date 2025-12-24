# COMMITTEE ONE-PAGER (SuayLang)

## Claim

**Primary claim:** SuayLang provides **two independent executions** (a reference interpreter and a bytecode VM) and a **reproducible protocol** to test observational equivalence under an explicit observation policy.

This one-pager is intentionally “paper-like”: every claim must map to a concrete evidence file and a reproduction command.

## Protocol

Canonical command (single entrypoint):

```sh
make reproduce-all
```

Alternative scripted entrypoint (reviewer-friendly):

```sh
bash ./scripts/reproduce.sh
```

Environment expectation:
- Linux + Python 3.12.x are the primary supported settings for the artifact pipeline.

## Evidence map (claim → artifact → reproduce)

| Claim surface | Evidence artifact(s) | Where to read | Reproduce |
|---|---|---|---|
| Observation policy (what is compared / ignored) | docs/OBSERVATION_POLICY.md | policy + falsification criteria | n/a |
| Equivalence (interpreter vs VM) | results/diff_report.md (and/or JSON when present) | divergence summary and counterexamples | `make reproduce-all` |
| Baseline suite timings | results/baseline.md + results/baseline_raw.json | per-program median runtimes | `make baseline` |
| Microbench (interp vs VM, relative) | benchmarks/results.md + docs/plots/microbench_relative.png | “example run” table + derived plot | `make plot-microbench` |
| Artifact integrity (hashes) | results/manifest.json + results/hashes.txt | per-artifact SHA-256 | `make hashes` |

## Where artifacts are

- Reviewer portal: docs/REVIEWER_PORTAL.md
- Claim↔evidence matrix: docs/CLAIM_EVIDENCE_MATRIX.md
- Artifact index: results/README.md
- Reproducibility contract (including “if results diverge”): docs/REPRODUCIBILITY.md
- Threats and limitations: docs/THREATS_TO_VALIDITY.md, docs/LIMITATIONS.md

## Notes for reviewers

- Numeric values are not asserted here; they are read from generated artifacts under results/.
- Any divergence or missing artifact is a falsification signal per docs/OBSERVATION_POLICY.md.
