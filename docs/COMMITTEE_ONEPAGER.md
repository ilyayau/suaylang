# SuayLang: Committee One-Pager

**Claim:**
Interpreter and VM executions for SuayLang are observationally equivalent under a fixed, auditable observation policy, evidenced by deterministic, reproducible experiments.

**Protocol:**
- All experiments are deterministic (fixed seeds, commit hash, environment recorded)
- One-command reproduction: `make reproduce`
- Output artifacts: results/*.md, results/*.json, paper/suaylang-tech-report.pdf

**Key Results:**
- 0 divergences, 5001 programs, 10 seeds, mean VM runtime 0.138s
- Differential test: [results/diff_report.md](../results/diff_report.md)
- Baseline: [results/baseline.md](../results/baseline.md)
- Coverage: [results/coverage.md](../results/coverage.md)
- Diagnostics: [results/golden_diagnostics.md](../results/golden_diagnostics.md)

**How to reproduce in 10 minutes:**
1. Clone the repo and install requirements (see README)
2. Run `make reproduce`
3. Inspect [results/README.md](../results/README.md) for all outputs

**Limitations:**
- Only tested on Linux, Python 3.13.11
- v0.1, single-threaded, no concurrency, no JIT, no optimizer
- Comparator ignores formatting, possible false negatives

**Artifact Index:**
- [results/README.md](../results/README.md) — canonical artifact index
- [docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) — threats and limitations

**Contact:** See [docs/contributions.md](contributions.md)
