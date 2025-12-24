#!/usr/bin/env bash
set -euo pipefail

PY=${PYTHON:-python}

rm -rf .cleanroom-venv
"$PY" -m venv .cleanroom-venv
source .cleanroom-venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev,plots]"

python -m ruff check .
python -m mypy
python -m pytest --cov=suaylang --cov-report=term-missing

make reproduce-fast PY=python
make verify-results PY=python

echo "clean-room-test: OK"
