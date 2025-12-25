# Evidence Map (Claim → Metric → Where → Result → Reproduce)

This table is **artifact-driven**: the “Result” column points to files under `results/` rather than repeating numbers in docs.

| Claim | Metric | Where computed | Result (artifact) | Reproduce |
|---|---|---|---|---|
| Observation policy is explicit and falsifiable | Declared observation set + explicit falsifier definition | docs/OBSERVATION_POLICY.md | docs/OBSERVATION_POLICY.md | n/a |
| Interpreter and VM are observationally equivalent (for shipped corpora) | Pass/fail equivalence; counterexample when failing | tools/diff_test + tools/conformance/run.py | results/diff_report.md and results/diff_report.json | `make reproduce-all` |
| Baseline suite provides reproducible timings | Median runtime across N runs per benchmark per backend | experiments/baseline_runner.py | results/baseline.md and results/baseline_raw.json | `make baseline` |
| Integrity metadata supports independent verification | SHA-256 per artifact + environment metadata | tools/gen_manifest.py + tools/gen_hashes.py + tools/verify_results.py | results/manifest.json and results/hashes.txt | `make reproduce-all` |

See also:

- Reviewer hub: docs/REVIEWER_PORTAL.md
- Artifact index: results/README.md
- Committee one-pager: docs/COMMITTEE_ONEPAGER.md
- Machine-readable map: docs/evidence_map.json
