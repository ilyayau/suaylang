# Benchmarks (SuayLang)

Backed by raw JSON in `results/bench_raw.json`.

- commit: `e67d94e22cc3565de8cc2e928c4c08eb2eeaff36`
- profile: `smoke`
- iters: 5 (per phase; per program)
- warmup: 1
- bench_dir: `/home/ayaubarys/Desktop/projects/suayLang/benchmarks/v1`
- python: 3.13.11 (main, Dec 15 2025, 10:06:06) [GCC 15.2.1 20251112]
- platform: Linux-6.17.9-arch1-1-x86_64-with-glibc2.42
- cpu: 12th Gen Intel(R) Core(TM) i5-12450H

## Summary table (ms)

All timings are median / p90.

| Program | Parse | Compile | Interp | VM | interp/vm (median) | VM instr | VM steps |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01_fibonacci.suay | 1.411/1.468 | 0.171/0.183 | 10648.597/10876.486 | 8400.460/8550.995 | 1.27 | 104 | 12 |
| 02_dispatch_heavy.suay | 1.918/1.925 | 0.310/0.317 | 20.462/20.953 | 26.820/27.007 | 0.76 | 180 | 14 |
| 03_cycle_state_machine.suay | 1.329/1.391 | 0.184/0.186 | 208.628/244.486 | 198.351/252.138 | 1.05 | 93 | 9 |
| 04_map_fold.suay | 0.819/0.834 | 0.086/0.107 | 0.323/0.328 | 0.250/0.265 | 1.29 | 54 | 46 |
| 05_string_and_collections.suay | 1.620/1.629 | 0.180/0.186 | 10.431/10.456 | 8.441/8.483 | 1.24 | 111 | 40 |
| 06_module_access.suay | 1.203/1.216 | 0.136/0.144 | 37.344/37.410 | 32.346/32.953 | 1.15 | 85 | 23 |

## Interpretation (10 bullets, no hand-waving)

- VM wins are expected when the same bytecode runs many steps (e.g., `cycle` / recursion), amortizing compile overhead.
- Interpreter can be competitive on tiny programs where parse/compile dominate and runtime is short.
- `dispatch` heavy benchmarks stress pattern matching and branching; they show whether opcode dispatch beats AST walking.
- `cycle` state-machine workloads are designed to be branchy but allocation-light; they tend to favor the VM.
- `map+fold` exercises higher-order builtins plus closure calls; results depend heavily on how often the backend crosses Python function boundaries.
- Text/Map workloads include `put/keys/has/text`; these are Python-implemented builtins and may reduce VM advantage (both backends pay Python cost).
- Module access uses repeated `link` calls; module caching helps, so this mostly measures cached lookup + call-site error framing overhead.
- p90 values make tail latency visible; if p90 diverges from median, noise (GC, CPU scheduling) is a likely contributor.
- Memory numbers are `tracemalloc` peaks (Python allocations), not RSS; treat them as relative signals only.
- This is a microbenchmark suite: it does not model I/O, large modules, or long-running real applications; use it for trends, not absolutes.
