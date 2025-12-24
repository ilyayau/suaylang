#!/bin/bash
set -e
python -m venv .venv
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  echo "ERROR: venv activation script not found. Ensure you are using bash/zsh, not fish."
  exit 1
fi
python -m pip install -U pip
python -m pip install -e ".[dev,plots]"
python -m pytest --cov=suaylang --cov-report=term-missing
if [ "$1" = "--full" ]; then
  make reproduce-all
else
  make reproduce-fast
fi
echo REPRODUCED OK
