# Experiments: Reproducible Evaluation

This directory contains the scripts and instructions for running all core experiments and regenerating results artifacts.

## How to run

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest -q
make research
```

## What is measured

## What “success” means

## Protocol


**See also:**
- 0 divergences in diff_report
