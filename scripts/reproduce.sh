#!/bin/sh
set -e
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
python -m pytest -q
if [ "$1" = "--full" ]; then
  make reproduce-all
else
  make research
fi
echo REPRODUCED OK
