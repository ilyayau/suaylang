# Reviewer path (15 minutes)

This path is optimized for a skeptical but fair reviewer who wants to understand:
- what SuayLang is,
- what is claimed,
- what evidence exists or is planned,
- how to reproduce core checks quickly.

## 1) Read (≈10 minutes)

1) Language contract (what v0.1 means):
- docs/LANGUAGE_CONTRACT_v0.1.md

2) Architecture overview:
- docs/ARCHITECTURE.md

3) Research hypothesis and evaluation methodology:
- docs/research/hypothesis.md
- docs/research/evaluation_plan.md
- docs/research/hypothesis_to_evidence.md

4) Unicode as a controlled variable:
- docs/research/unicode_tradeoff.md

## 2) Run (≈5 minutes)

From the repository root:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"

pytest -q
python scripts/smoke.py

# Optional: packaging sanity
python -m build
python -m twine check dist/*
```

Interpretation:
- `pytest` ensures core semantics tests pass.
- `scripts/smoke.py` enforces the “no Python tracebacks” CLI UX constraint on representative examples.

## Notes on scope

- The interpreter is the baseline semantics for v0.1.
- VM equivalence claims, when made, are scoped to a documented subset.
