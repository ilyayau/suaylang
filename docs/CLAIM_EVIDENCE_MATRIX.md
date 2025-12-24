# Claim–Evidence Matrix (SuayLang)

| Claim | Where Stated | Evidence Files | Command to Reproduce | Result to Read | Failure Mode |
|-------|--------------|---------------|---------------------|----------------|--------------|
| Interpreter and VM executions are observationally equivalent under a fixed, auditable observation policy | README.md, docs/COMMITTEE_ONEPAGER.md, docs/TECH_REPORT.md | results/diff_report.md (and/or JSON when present) | `make reproduce-all` | Read divergence count and any counterexample traces | Any nonzero divergences reported |
| Coverage is computed and reported as an artifact (do not hard-code counts) | docs/TECH_REPORT.md | results/coverage.md (when produced) | `make reproduce-all` | Read coverage tables in coverage.md | Missing coverage artifact or unexpected gaps |
| Baseline suite produces per-program timing table | README.md, docs/COMMITTEE_ONEPAGER.md | results/baseline.md, results/baseline_raw.json | `make baseline` | Read per-program medians | Missing programs, nonzero exit codes, missing output files |
| Microbench example run (interp vs VM) | benchmarks/results.md, docs/COMMITTEE_ONEPAGER.md | docs/plots/microbench_relative.png | `make plot-microbench` | Plot derived from the checked-in table | Plot generation fails or plot missing |
| Artifact integrity is recorded via hashes | docs/COMMITTEE_ONEPAGER.md, results/README.md | results/manifest.json, results/hashes.txt | `make hashes` | Hashes for evidence files are present | Missing hashes or mismatch after regeneration |

- Evidence is indexed in results/README.md.
- The canonical reproduction command is `make reproduce-all`.
