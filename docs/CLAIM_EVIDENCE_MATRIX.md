# Claim–Evidence Matrix (SuayLang)

| Claim | Where Stated | Evidence Files | Command to Reproduce | Expected Output | Failure Mode |
|-------|--------------|---------------|---------------------|----------------|--------------|
| Interpreter and VM executions are observationally equivalent under a fixed, auditable observation policy | README.md, COMMITTEE_ONEPAGER.md, TECH_REPORT.md | results/diff_report.md, results/diff_report.json | ./scripts/reproduce.sh or make research | 0 divergences, 5001 programs, 10 seeds | Any nonzero divergences in diff_report.md/json |
| Coverage: 24 AST, 20 opcodes | README.md, COMMITTEE_ONEPAGER.md, TECH_REPORT.md | results/coverage.md, results/coverage.json | ./scripts/reproduce.sh or make research | Coverage tables: 24 AST, 20 opcodes | Lower coverage, missing constructs/opcodes |
| Baseline: 5 programs, timings | README.md, COMMITTEE_ONEPAGER.md, TECH_REPORT.md | results/baseline.md | ./scripts/reproduce.sh or make research | Table with 5 programs, timings for Python, SuayInterp, SuayVM | Missing/incorrect timings, missing programs |
| Benchmarks: 6 programs, runtime, memory | TECH_REPORT.md, benchmarks.md | results/benchmarks.md, results/bench_raw.json | ./scripts/reproduce.sh or make research | Benchmark tables, raw JSON | Missing/incorrect benchmarks |
| Diagnostics contract: error kind, code, span | TECH_REPORT.md, COMMITTEE_ONEPAGER.md | results/golden_diagnostics.md, results/golden_diagnostics.json | ./scripts/reproduce.sh or make research | All tests pass (6/6) | Test failures, missing diagnostics |
| Mutation/injection validation | TECH_REPORT.md | results/mutation_catches.md | ./scripts/reproduce.sh or make research | Table: all injected faults caught | Missed faults, uncaught errors |
| Ablation: control-flow-as-expr, diagnostics degraded | TECH_REPORT.md | results/ablation.md, ablation_raw.json | ./scripts/reproduce.sh or make research | Table: ablation results | No ablation, missing/incorrect results |
| Coverage by construct | TECH_REPORT.md | results/coverage_by_construct.md | ./scripts/reproduce.sh or make research | Table: all constructs covered | Missing constructs, gaps |
| Environment, commit, artifact hashes | manifest.json, environment.md/json | results/manifest.json, results/environment.md, results/environment.json | ./scripts/reproduce.sh or make research | All metadata present, hashes match | Missing/incorrect metadata |

- All evidence files are referenced in results/README.md (artifact index).
- All commands are deterministic and documented in README.md and ARTIFACT_EVALUATION.md.
- Failure modes are reviewer-facing: any deviation is visible in the corresponding evidence file.
