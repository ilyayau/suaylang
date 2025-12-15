# Testing

SuayLang’s test suite aims to provide two kinds of confidence:

1) **Behavior tests**: language semantics and error behavior stay stable.
2) **Trust tests**: the CLI never leaks Python tracebacks and reports spans cleanly.

## Quick commands

From the repo root:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

Run all tests:

```sh
pytest -q
```

Run smoke checks (examples + error UX):

```sh
python scripts/smoke.py
```

Run lint + formatting checks:

```sh
ruff check .
ruff format --check .
```

## Property-based tests

Some tests use Hypothesis to generate many small inputs. These are intentionally bounded (small integers, limited examples) to keep CI fast and deterministic.

## Interpreter vs VM equivalence

Where applicable, tests compare the interpreter’s result to the bytecode VM’s result for a supported subset. This is meant to catch semantic drift between the two execution paths.
