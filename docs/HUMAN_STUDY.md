# Human-facing experiment (proxy) — SuayLang v0.1

A full human study (5–10 participants) is ideal, but often infeasible for a small research artifact.
This repository therefore provides a **defensible proxy protocol with real, reproducible data** derived from paired programs implementing the same micro-tasks in SuayLang and a baseline language (Python).

## Goal

Assess whether SuayLang’s expression-based control flow (dispatch/cycle) and explicit binding/mutation reduce *surface complexity* for small tasks.

This is **not** a claim about human comprehension by itself; it is a proxy that can be run in CI and provides falsifiable signals.

## Proxy protocol

### Inputs

Paired task programs under `evaluation/human_proxy/`:

- `*.suay` (SuayLang)
- `*.py` (baseline)

Each pair implements the same task with similar constraints.

### Metrics (computed automatically)

For each program we compute:

- LOC / non-empty LOC
- token count (regex-based approximation)
- maximum delimiter nesting depth (proxy for structural complexity)
- number of control-flow markers (SuayLang: `|>`, `~~`; Python: `if/elif/else/while/for/match`)
- “surface operator diversity” (distinct operator tokens)

Implementation: `tools/human_proxy/run.py`.

### Output data

- Raw CSV: `results/human_study.csv`
- Summary: `results/human_study.md`

Run:

- `make human-study`

## Interpretation rules

We interpret the proxy as supporting evidence when, across task pairs:

- SuayLang shows **lower or comparable** non-empty LOC and token count,
- and **lower control-flow marker count** for the same task,
- without increased nesting depth.

## Threats to validity (explicit)

- Proxy metrics are not human comprehension measurements.
- Pair quality matters: different idioms in Python can change counts.
- Tokenization is approximate.
- Results apply to small tasks only; they do not imply maintainability at scale.

Future work:
- Run Option A with 5–10 participants and publish anonymized time/correctness + Likert ratings.
