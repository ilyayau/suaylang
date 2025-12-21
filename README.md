


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
