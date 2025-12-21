



# SuayLang: Committee-Grade Research Artifact

**Committee TL;DR (60 seconds)**

- **Claim:** Interpreter and VM executions for SuayLang are observationally equivalent under a fixed, auditable observation policy, evidenced by deterministic, reproducible experiments.
- **Evidence:**
	- [Diff test: 0 divergences, 5001 programs, 10 seeds](results/diff_report.md)
	- [Baseline: 5 programs, timings in results/baseline.md](results/baseline.md)
	- [Coverage: 24 AST, 20 opcodes, results/coverage.md](results/coverage.md)
**Evidence:**
**Reproduce (fast):** `bash ./scripts/reproduce.sh`
**Reproduce (full):** `bash ./scripts/reproduce.sh --full`
---

**Observation Policy:** See [docs/OBSERVATION_POLICY.md](docs/OBSERVATION_POLICY.md) for the formal definition of what is compared, what is ignored, and how the claim can be falsified. This policy is the contract for all equivalence evidence.

**So what?**
SuayLang demonstrates that a research language can achieve bit-for-bit equivalence between interpreter and VM backends, under a transparent, reviewer-auditable observation policy. This artifact sets a new bar for reproducibility, evidence integrity, and reviewer experience in PL artifact evaluation.
3. Inspect: [results/README.md](results/README.md) (artifact index)
## Shell Requirements

All reproduction scripts require bash or zsh (not fish). If you use fish, run `bash ./scripts/reproduce.sh` explicitly.

## Reproduction Receipt

**Environment:**
- OS: Linux (tested)
- Python: 3.12.x (venv created automatically)
- Shell: bash or zsh required

**Commands:**
- Fast: `bash ./scripts/reproduce.sh`
- Full: `bash ./scripts/reproduce.sh --full`

**Expected outputs:**
- All results land in results/ (diff_report.md/json, baseline.md, coverage.md, benchmarks.md, golden_diagnostics.md, ablation.md, mutation_catches.md, manifest.json, environment.md/json)

**Failure modes:**
- Shell error: Use bash, not fish
- Python version error: Use Python 3.12.x
- Missing results: Check for errors in output, rerun with correct environment

4. Read: [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) (1-page summary)
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


## Portable Reproduction (Docker)

To guarantee a clean, portable environment, you can run all artifact experiments in Docker:

```sh
docker build -t suaylang-artifact .
docker run --rm -it suaylang-artifact
```

This will execute the full reproduction pipeline in a containerized Python 3.12 + bash/zsh environment, with all dependencies pre-installed. See the Dockerfile for details.

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
