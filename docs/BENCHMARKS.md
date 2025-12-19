# Benchmarks

SuayLang includes a small benchmark script intended for **honest, reproducible** microbenchmarks.

Goals:

- Compare interpreter vs VM on small example programs.
- Separate parsing from execution where possible.

Non-goals:

- Producing publishable performance claims.
- Optimizing microbenchmarks for best-looking numbers.

## How to run

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"

python benchmarks/benchmark_runner.py --profile full --out-dir results

# Smoke profile (CI-like)
python benchmarks/benchmark_runner.py --profile smoke --out-dir results

# Outputs:
# - results/bench_raw.json
# - results/benchmarks.md
```

## Methodology notes

- Benchmarks are sensitive to machine load, Python version, and CPU frequency scaling.
- The script performs a small warm-up and reports median timings.
- Results should be interpreted as “relative signals” rather than absolute truths.

## What’s measured

- Lex+parse time for a program (shared front-end cost).
- Interpreter execution time.
- Compiler+VM execution time (compiler cost reported separately).
