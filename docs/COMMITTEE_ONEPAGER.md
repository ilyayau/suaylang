# SuayLang: Committee One-Pager

**Claim:** Interpreter and VM executions for SuayLang are observationally equivalent under a fixed, auditable observation policy, evidenced by deterministic, reproducible experiments.

**Method:**
- Deterministic differential testing (fixed seeds, commit hash, env capture)
- Diagnostics contract (error kind, code, span)
- Coverage analysis (24 AST, 20 opcodes)
- Baseline and ablation comparison
- Mutation/injection validation

**Results:**
- 0 divergences, 5001 programs, 10 seeds ([results/diff_report.md](../results/diff_report.md))
- Baseline: 5 programs, timings ([results/baseline.md](../results/baseline.md))
- Coverage: 24 AST, 20 opcodes ([results/coverage.md](../results/coverage.md))

**Reproduce:**
1. Clone: `git clone https://github.com/ilyayau/suaylang && cd suaylang`
2. Run: `./scripts/reproduce.sh` (fast) or `--full`
3. Inspect: [results/README.md](../results/README.md)

**Limitations:**
- Only tested on Linux, Python 3.12.x
- v0.1, single-threaded, no concurrency/JIT/optimizer
- Comparator ignores formatting, possible false negatives
