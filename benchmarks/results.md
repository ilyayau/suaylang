# Micro-benchmarks (interpreter vs VM)

This directory contains a small, intentionally conservative micro-benchmark suite.

## Methodology

- Same SuayLang program is executed in:
  - the reference interpreter, and
  - the bytecode VM.
- Timing uses wall-clock `time.perf_counter()`.
- Reported time is the **median** over `--iters` iterations, after a short warm-up.
- The VM instruction count is the number of compiled bytecode instructions (`len(code.instrs)`).

Reproduce (from repo root):

- `python scripts/bench_micro.py --iters 50 benchmarks/fib benchmarks/map_fold benchmarks/dispatch benchmarks/cycle`

## Results (example run)

These measurements are machine-dependent; treat **Relative** as the primary signal.

| Program | Interpreter (ms) | VM (ms) | Relative (interp/vm) | VM instr | Notes |
|---|---:|---:|---:|---:|---|
| fib | 0.739 | 0.666 | 1.11 | 60 | iterative cycle, integer arithmetic |
| map_fold | 42.121 | 35.505 | 1.19 | 81 | builtin `map`+`fold` + list building |
| dispatch_chain | 80.950 | 67.770 | 1.19 | 89 | dispatch-heavy branching |
| cycle_sum | 127.287 | 113.551 | 1.12 | 58 | explicit state-machine summation |

Environment notes:

- These numbers were collected on the local developer machine (Linux) and are not expected to match CI.
- The timing harness measures end-to-end execution in the current Python runtime; treat the VM as an execution strategy, not a speed guarantee.
