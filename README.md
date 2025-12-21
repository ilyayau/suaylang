


<h1 align="center">SuayLang: Committee-Grade Research Artifact</h1>

<p align="center"><b>Interpreter and VM executions for SuayLang are observationally equivalent under a fixed, auditable observation policy, evidenced by deterministic, reproducible experiments.</b></p>

<p align="center"><img src="showcase/demo.gif" alt="Demo: install, doctor, run, research" width="500"></p>

---

## Committee 10-Line Summary

1. **Problem:** Most small languages lack falsifiable, reviewer-auditable backend equivalence and diagnostics stability.
2. **Research Question:** Can interpreter and VM executions be made observationally equivalent (value, error, stdout) on a large, seeded program set?
3. **Hypotheses:** (H1) Interpreter and VM are observationally equivalent on all programs in the test suite. (H2) Diagnostics are stable and contractually enforced for all golden cases.
4. **Method:** Deterministic differential testing, diagnostics contract, coverage analysis, baseline/ablation, mutation/injection validation.
5. **Protocol:** All experiments are deterministic (fixed seeds, commit hash, environment recorded). One-command reproduction: `make reproduce`.
6. **Key Results:** 0 divergences, 5001 programs, 10 seeds, mean VM runtime 0.138s. See [results/diff_report.md](results/diff_report.md).
7. **Evidence:** All metrics and artifacts in [results/README.md](results/README.md). Baseline: [results/baseline.md](results/baseline.md). Coverage: [results/coverage.md](results/coverage.md). Diagnostics: [results/golden_diagnostics.md](results/golden_diagnostics.md).
8. **Limitations:** Only tested on Linux, Python 3.13.11. v0.1, single-threaded, no concurrency/JIT/optimizer. Comparator ignores formatting, possible false negatives. See [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md).
9. **Why it matters:** Demonstrates a reproducible, committee-proof artifact pipeline for language research.
10. **How to reproduce:** Clone, install requirements, run `make reproduce`, inspect [results/README.md](results/README.md).

---

## 15-Minute Reviewer Path

1. **Clone and install:** See below for requirements.
2. **Run:** `make reproduce` (runs all tests, conformance, diff-test, baseline, ablation, builds PDFs)
3. **Inspect:** [results/README.md](results/README.md) — all metrics and evidence
4. **Read:** [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) (1-page summary)
5. **Open:** [paper/suaylang-tech-report.pdf](paper/suaylang-tech-report.pdf) — canonical report

---

## Evidence Map

- **Artifact index:** [results/README.md](results/README.md)
- **One-pager:** [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md)
- **Threats to validity:** [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md)
- **Tech report:** [docs/TECH_REPORT.md](docs/TECH_REPORT.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Roadmap:** [ROADMAP.md](ROADMAP.md)
- **Full results:** [results/](results/)

---

## Language Overview

SuayLang is a minimal, research-focused language and VM for studying backend equivalence and diagnostics contracts. It features:
- Expression-oriented, statically scoped syntax
- Deterministic interpreter and VM backends
- Explicit diagnostics contract (error kind, code, span)
- Differential testing, coverage, and ablation harnesses
- Reproducible artifact pipeline (see [results/README.md](results/README.md))

---

## Contributions

- **Tolkynkhan Sultanbarys:** Language design/specification, frontend pipeline (lexer, parser, AST), diagnostics, language examples, documentation.
- **Syrlybai Ayaulym:** Runtime/VM, memory model, CLI/REPL, developer workflow, CI, runtime-facing tests/benchmarks, demo reliability.

---

## CI & Artifact

[![CI](https://github.com/ilyayau/suaylang/actions/workflows/artifact.yml/badge.svg)](https://github.com/ilyayau/suaylang/actions/workflows/artifact.yml)

- **Latest CI artifact:** See [results/README.md](results/README.md) for all outputs. Artifacts are uploaded on every commit.

---

## Quickstart (moved)

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for install and usage details.

---

## For Reviewers

- [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) — 1-page summary
- [results/README.md](results/README.md) — artifact index
- [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md) — threats/limitations
- [docs/TECH_REPORT.md](docs/TECH_REPORT.md) — full report

---

## License & Citation

- [LICENSE](LICENSE)
- [CITATION.cff](CITATION.cff)


## 7-Minute Reviewer Path
1. `make reproduce` — runs all tests, conformance, diff-test, baseline, ablation, builds PDFs
2. Inspect [results/](results/README.md) — all metrics and evidence
3. Open [paper/suaylang-tech-report.pdf](paper/suaylang-tech-report.pdf) — canonical report

## Experimental Protocol
- All experiments are deterministic (fixed seeds, commit hash, environment recorded)
- One-command reproduction: `make reproduce`
- Output artifacts: results/*.md, results/*.json, paper/suaylang-tech-report.pdf


See: [Related Work — Architecture & Research Flow](docs/RELATED_WORK.md#architecture--research-flow)

**What reviewers usually misunderstand:**
- Observation policy is defined and enforced (see [Formal Summary](docs/FORMAL_SUMMARY_1PAGE.md)).
- Diagnostics contract is not just error codes, but spans and determinism.
- Equivalence is on value, error (code+span), and stdout, not just output text.
- Human-proxy metrics are included, but not a full user study.
- Baseline and ablation are real, not synthetic.

**Why this is NOT overengineering:**
- Every artifact is directly tied to a research claim or reviewer need.
- No superfluous features; all code and docs are minimal for the contract.
- All results are reproducible and evidenced.

**Audience:** Designed for PL researchers / reviewers, not end users.

**Reviewer checklist:** [docs/REVIEWER_CHECKLIST.md](docs/REVIEWER_CHECKLIST.md)

---

**Thesis claim:**
We show that interpreter↔VM observational equivalence and a stable diagnostics contract can be achieved with explicit, expression-oriented control flow, while preserving scorable evidence under a fixed observation policy and deterministic artifact pipeline. ([THESIS_CLAIM.md](docs/THESIS_CLAIM.md))

**Problem:** Most small languages claim “clear semantics” and “tooling-first design,” but backend equivalence and diagnostics stability are rarely falsifiable or reviewer-auditable.

**Research Questions:**
- RQ1: Can interpreter and VM executions be made observationally equivalent (value, error, stdout) on a large, seeded program set?
- RQ2: Can diagnostics (error kind, code, span) be made stable and contractually enforced?

**Hypotheses:**
- H1: Interpreter and VM are observationally equivalent on all programs in the test suite.
- H2: Diagnostics are stable and contractually enforced for all golden cases.

**Contributions:**
- Deterministic differential testing ([results/diff_report.md](results/diff_report.md))
- Golden diagnostics contract ([results/golden_diagnostics.md](results/golden_diagnostics.md))
- Coverage by construct ([results/coverage_by_construct.md](results/coverage_by_construct.md))
- Baseline and ablation comparison ([results/baseline.md](results/baseline.md), [results/ablation.md](results/ablation.md))
- Mutation/injection validation ([results/mutation_catches.md](results/mutation_catches.md))
- Human-proxy static metrics ([docs/HUMAN_PROXY.md](docs/HUMAN_PROXY.md))

**If you read only one thing:** See [docs/THESIS_CLAIM.md](docs/THESIS_CLAIM.md)

[See: docs/RESEARCH_FRAMING.md](docs/RESEARCH_FRAMING.md)

[![CI](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml/badge.svg)](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)