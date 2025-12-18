# Conformance (interpreter ↔ VM)

## What conformance means

SuayLang treats the interpreter as the reference behavior.

The bytecode VM must be observationally equivalent to the interpreter on the **supported subset** defined by the conformance suite.

Observations compared:
- termination class (`ok`, `lex`, `syntax`, `runtime`)
- stdout
- returned value (when `ok`)
- stable error code + primary span location (when failing)

## Where tests live

- Corpus programs: `conformance/corpus/*.suay`
- Pytest equivalence runner: `tests/conformance/`
- Golden diagnostics snapshots: `tests/golden/diagnostics/`

## How to run

From a dev install:

- `pytest -q`
- `python tools/conformance/run.py conformance/corpus`

CI runs both and publishes artifacts.

## Adding a new conformance case

1) Add a `.suay` file under `conformance/corpus/`.
2) Ensure it is in the supported subset for both backends.
3) If it is a negative test (expected failure), ensure the stable error code is documented in [docs/ERROR_CODES.md](ERROR_CODES.md) and add a golden diagnostic snapshot when appropriate.
