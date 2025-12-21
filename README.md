



# SuayLang: Committee-Grade Research Artifact

**Committee TL;DR (60 seconds)**

- **Claim:** Interpreter and VM executions for SuayLang are observationally equivalent under a fixed, auditable observation policy, evidenced by deterministic, reproducible experiments.
- **Evidence:**
	- [Diff test: 0 divergences, 5001 programs, 10 seeds](results/diff_report.md)
	- [Baseline: 5 programs, timings in results/baseline.md](results/baseline.md)
	- [Coverage: 24 AST, 20 opcodes, results/coverage.md](results/coverage.md)
- **Reproduce (fast):** `./scripts/reproduce.sh`
- **Reproduce (full):** `./scripts/reproduce.sh --full`

---

## 15-minute reviewer path

1. Clone: `git clone https://github.com/ilyayau/suaylang && cd suaylang`
2. Run: `./scripts/reproduce.sh` (or `--full`)
3. Inspect: [results/README.md](results/README.md) (artifact index)
4. Read: [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) (1-page summary)
5. See: [docs/ARTIFACT_EVALUATION.md](docs/ARTIFACT_EVALUATION.md) (AE guide)
6. See: [docs/TECH_REPORT.md](docs/TECH_REPORT.md) (mini tech report)
7. See: [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md) (threats/limitations)

---

## Evidence map

- [results/README.md](results/README.md) — artifact index
- [docs/ARTIFACT_EVALUATION.md](docs/ARTIFACT_EVALUATION.md) — AE guide
- [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) — one-pager
- [docs/TECH_REPORT.md](docs/TECH_REPORT.md) — tech report
- [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md) — threats/limitations
- [CHANGELOG.md](CHANGELOG.md) — changelog
- [ROADMAP.md](ROADMAP.md) — roadmap

---

## Scope / Non-goals

- Only tested on Linux, Python 3.13.11
- v0.1, single-threaded, no concurrency, no JIT, no optimizer
- Comparator ignores formatting, possible false negatives
- No IDE plugin, no web demo, no user study (see ROADMAP)
- Language/engineering details: [docs/overview.md](docs/overview.md)

---

## How to cite

- [CITATION.cff](CITATION.cff)
- [docs/refs.bib](docs/refs.bib)

---

## CI & Artifacts

[![CI](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml/badge.svg)](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml)

- Evidence artifacts are attached to every CI run (see Actions tab)

---

## For language/engineering details

See [docs/overview.md](docs/overview.md)
