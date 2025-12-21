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
python -m pip install -e .
python -m pip install pytest
python -m pytest -q
if [ "$1" = "--full" ]; then
  make reproduce-all
else
  make research
fi
echo REPRODUCED OK
