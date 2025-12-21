#!/bin/sh
set -e
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e .
python -m pytest -q
if [ "$1" = "--full" ]; then
  make reproduce-all
else
  make research
fi
echo REPRODUCED OK
