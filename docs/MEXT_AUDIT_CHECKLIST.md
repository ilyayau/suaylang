# MEXT 8/10 Audit Checklist (internal)

This document is a maintainer-facing checklist for raising SuayLang’s trust signals, reproducibility, and research clarity to an “8/10” level for skeptical technical review.

## Baseline (current state)

- Install: `python -m venv .venv && . .venv/bin/activate && pip install -e .`
- CLI (from source checkout): `./suay --help`
- CLI (installed): `python -m suaylang --help` or `suay --help`
- Quick demo: `./suay run examples/hello.suay` prints `total=30`
- Tests:
  - Legacy runner: `python -m unittest discover -s tests -v`
  - Pytest-compatible: `pytest -q` (runs existing suite)

## MUST-FIX items for 8/10

### Reproducibility + evaluation speed
- Provide a 10–15 minute reviewer path: install → run demo → run tests → run smoke.
- Add a deterministic smoke script that:
  - runs 3–5 canonical example programs,
  - validates stdout exactly,
  - validates that error cases are human-readable and contain no Python tracebacks.
- Add a single-command dev UX via Makefile targets (install/test/lint/format/smoke/build).

### Trust signals (GitHub-facing)
- CI that runs on push/PR and fails on any issue:
  - `ruff check`, `ruff format --check`, `pytest`, smoke, `python -m build`.
- README badges: CI, Python version, license.
- Add CHANGELOG.md (Keep a Changelog) and a release procedure doc.
- Add CITATION.cff for academic citation.
- Add CODEOWNERS.
- Add an owner checklist for GitHub “About”/topics/settings (can’t be done by automation reliably).

### Research clarity (MEXT-facing)
- Add concise, reviewer-targeted docs:
  - Architecture overview (execution pipeline + modules + error strategy).
  - Research note (problem statement, novelty, metrics, limitations).
  - Benchmarks (simple methodology + honest limitations).

### Testing discipline
- Keep existing tests green.
- Add targeted new tests (>=20) and a few property tests (Hypothesis) focused on:
  - parsing edge cases,
  - error reporting shape (no tracebacks),
  - interpreter vs VM equivalence for supported subset,
  - stdlib behavior invariants.
- Document the testing strategy and which parts are intended as “trust tests” vs “behavior tests”.

## SHOULD-FIX (nice-to-have, if time)
- Ensure build artifacts are ignored (`dist/`, `build/`, `*.egg-info/`).
- Tighten VS Code extension README (what works, how to install locally).
