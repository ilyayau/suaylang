# Evidence Map (Claim → Metric → Where → Result → Reproduce)

This table is **artifact-driven**: the “Result” column points to files under `results/` rather than repeating numbers in docs.

| Claim | Metric | Where computed | Result (artifact) | Reproduce |
|---|---|---|---|---|
| Observation policy is explicit and falsifiable | Presence + stable interpretation of what is observed/ignored | docs/OBSERVATION_POLICY.md | docs/OBSERVATION_POLICY.md | n/a |
| Interpreter and VM are observationally equivalent (for shipped corpora) | Pass/fail equivalence over corpora; counterexample if fail | tools/diff_test + conformance corpus | results/ (diff-test outputs, conformance summaries) and results/README.md | `make diff-test-ci` (or `make reproduce-all`) |
| Baseline suite provides reproducible timings | Per-program median runtime (Python vs interpreter vs VM) | experiments/baseline_runner.py | results/baseline.md and results/baseline_raw.json | `make baseline` |
| A committed plot is generated from artifacts | Image regenerated from results/baseline_raw.json and/or benchmarks/results.md | tools/plot_results.py and tools/plot_microbench.py | docs/plots/interp_vs_vm.png and docs/plots/microbench_relative.png | `make plots` and `make plot-microbench` |
| Integrity metadata supports independent verification | SHA-256 over key artifacts | tools/gen_hashes.py and tools/gen_manifest.py | results/hashes.txt and results/manifest.json | `make hashes` and `make manifest` |

See also:

- Reviewer hub: docs/REVIEWER_PORTAL.md
- Artifact index: results/README.md
- Committee one-pager: docs/COMMITTEE_ONEPAGER.md
