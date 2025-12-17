# Reviewer Path (15 minutes)

This document is a **committee-facing path**: what to read, what to run, and what evidence each command produces.

## 0) One-minute orientation (read)

- [docs/reviewer/EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) — problem, research questions, hypotheses, methods, snapshot results.
- [docs/research/RESEARCH_CORE.md](../research/RESEARCH_CORE.md) — falsification criteria, scope control, threats.

## 1) Install (2 minutes)

From repo root:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

Evidence:

- A local environment that can run tests and evaluation scripts.

## 2) Run tests (3 minutes)

```sh
pytest -q
```

Evidence:

- Parser/lexer/runtime correctness tests.
- Golden diagnostics regression tests (stable error messages + spans).

## 3) H2: interpreter↔VM equivalence (5 minutes)

### 3.1 Conformance (fixed corpora)

```sh
python tools/conformance/run.py
python tools/conformance/run.py evaluation/tasks
python tools/conformance/run.py conformance/corpus
```

Evidence:

- A single-line summary of **files** and **divergences**.
- Any divergence prints an explicit counterexample with interpreter vs VM observations.

### 3.2 Differential fuzz (seeded)

```sh
python -m tools.conformance.fuzz --seed 0 --n 1000 --raw
```

Evidence:

- A single-line numeric summary: seed, N, divergences.
- Raw run log written under `data/raw/fuzz_runs/` (JSONL).

### 3.3 One-line H2 summary (paper-friendly)

```sh
python tools/research/h2_eval.py --seed 0 --n 1000
```

Evidence:

- A compact summary line suitable for copying into reports.

## 4) H1 (optional): structural proxy metrics (3 minutes)

```sh
python tools/metrics/h1_metrics.py --out docs/research/H1_metrics_table.md
```

Evidence:

- A fixed 5-task SuayLang vs Python table (tokens, approx AST depth, branch points).

## 5) Coverage matrix (2 minutes)

```sh
python tools/coverage/coverage_report.py
```

Evidence:

- `docs/research/coverage_matrix.md` (human-readable table)
- `data/raw/coverage_matrix.csv` (raw matrix)

## 6) Read the “paper kit” (optional, ~10 minutes)

- [docs/paper/suaylang_paper.md](../paper/suaylang_paper.md)
