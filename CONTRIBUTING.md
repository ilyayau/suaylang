# Contributing to SuayLang

This repository is a language implementation intended for external review. Contributions are welcome, but the bar is intentionally strict: changes should be small, readable, and backed by tests.

## Quick setup (development)

Prerequisites:

- Python 3.10+

From a clean clone:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

# editable install (provides the `suay` CLI)
python -m pip install -e ".[dev]"

# sanity check
suay doctor

## Pre-commit hooks

This repo uses `pre-commit` to enforce formatting, lint, and basic file hygiene.

Install the git hooks:

```sh
pre-commit install
```

Run on all files:

```sh
pre-commit run --all-files
```
```

## Running tests

pytest -q
python -m unittest discover -s tests -v
```

## Running examples

```sh
suay run examples/committee_01_basic.suay
suay run examples/committee_02_dispatch.suay
suay run examples/committee_03_cycle.suay
```

## Contribution guidelines

### Scope discipline

- Do not redesign the language surface without discussion.
- Prefer bug fixes, diagnostics improvements, tests, and documentation.
- Keep patches minimal and reviewable.

### Quality requirements

A contribution is expected to:

- keep `python -m unittest discover -s tests -v` green,
- preserve the “no Python tracebacks” user experience from the CLI,
- include tests for user-visible behavior changes,
- update docs when changing semantics, syntax, or builtins.

### Commit and PR style

- One change per PR when possible.
- Write PR descriptions that include:
  - motivation,
  - what changed,
  - how to verify.
- Avoid drive-by refactors (renames/reformatting) mixed with semantic changes.

## Reporting issues

If you found a bug:

- include a minimal `.suay` snippet,
- include the exact command you ran,
- include the full CLI output.

If you suspect a security issue, see `SECURITY.md`.
