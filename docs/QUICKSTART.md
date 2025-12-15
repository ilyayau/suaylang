# Quickstart (15-minute reviewer path)

This quickstart is designed for skeptical reviewers: install, run a demo, run tests, and confirm error UX (no Python tracebacks).

## 1) Setup (clean machine)

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## 2) Sanity check

```sh
suay doctor
```

Expected output includes a line `doctor:ok` followed by `OK`.

## 3) Quick demo

```sh
suay run examples/hello.suay
```

Expected output:

```text
total=30
```

## 4) Run tests

```sh
pytest -q
```

## 5) Run smoke checks (examples + error UX)

```sh
python scripts/smoke.py
```

Expected output:

```text
smoke:ok
```

## 6) Build artifacts (wheel + sdist)

```sh
python -m build
```

Artifacts appear under `dist/`.
