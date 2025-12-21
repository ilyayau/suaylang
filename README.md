



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
6. See: [docs/TECH_REPORT.md](docs/TECH_REPORT.md) (mini tech report; PDF: see below)
7. See: [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md) (threats/limitations)
8. See: [docs/CLAIM_EVIDENCE_MATRIX.md](docs/CLAIM_EVIDENCE_MATRIX.md) (claim–evidence matrix)
9. See: [docs/REVIEWER_PORTAL.md](docs/REVIEWER_PORTAL.md) (reviewer portal)

---

## Evidence map

- [results/README.md](results/README.md) — artifact index
- [docs/ARTIFACT_EVALUATION.md](docs/ARTIFACT_EVALUATION.md) — AE guide
- [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) — one-pager
- [docs/TECH_REPORT.md](docs/TECH_REPORT.md) — tech report (PDF: see below)
- [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md) — threats/limitations
- [CHANGELOG.md](CHANGELOG.md) — changelog
- [ROADMAP.md](ROADMAP.md) — roadmap

---


## Scope / Non-goals

- Only tested on Linux, Python 3.12.x
- v0.1, single-threaded, no concurrency, no JIT, no optimizer
- Comparator ignores formatting, possible false negatives
- IDE plugin exists (vscode-extension/), but is WIP and not part of evaluated claims for v0.1. No web demo, no user study (see ROADMAP)
- Language/engineering details: [docs/overview.md](docs/overview.md)

## Supported Python Versions

SuayLang is tested and supported on Python 3.12.x. All CI and reproduction commands use Python 3.12. Other versions are not guaranteed to work.

---

## How to cite

- [CITATION.cff](CITATION.cff)
- [docs/refs.bib](docs/refs.bib)

---

## CI & Artifacts


[![CI](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml/badge.svg)](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml)

- Evidence artifacts are attached to every CI run (see Actions tab)

---

## Technical Report PDF

- The canonical tech report is [docs/TECH_REPORT.md](docs/TECH_REPORT.md).
- To generate the PDF: `make tech-report-pdf` (requires pandoc + xelatex; output: `paper/suaylang-tech-report.pdf`).
- If the PDF is missing, see the markdown version above. The PDF is attached to releases and CI artifacts when available.

## Link check

- To check all internal markdown links: `sh scripts/check_links.sh` (returns nonzero if any are broken).

---

## For language/engineering details

See [docs/overview.md](docs/overview.md)
