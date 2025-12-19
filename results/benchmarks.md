# Benchmarks (SuayLang)

Backed by raw JSON in `results/bench_raw.json`.

- commit: `ae3e32ee0f9e63f41798de93a2c9de71832d12cb`
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
| 01_fibonacci.suay | 1.563/1.611 | 0.183/0.202 | 5143.035/7265.284 | 3953.327/3986.542 | 1.30 | 104 | 12 |
| 02_dispatch_heavy.suay | 0.933/0.945 | 0.146/0.150 | 9.446/9.795 | 12.579/13.058 | 0.75 | 180 | 14 |
| 03_cycle_state_machine.suay | 0.618/0.643 | 0.082/0.084 | 99.389/100.466 | 93.526/95.387 | 1.06 | 93 | 9 |
| 04_map_fold.suay | 0.416/0.436 | 0.042/0.044 | 0.172/0.189 | 0.130/0.145 | 1.32 | 54 | 46 |
| 05_string_and_collections.suay | 0.826/0.864 | 0.089/0.093 | 5.536/5.721 | 4.357/4.528 | 1.27 | 111 | 40 |
| 06_module_access.suay | 0.590/0.608 | 0.069/0.073 | 19.194/20.048 | 16.671/16.730 | 1.15 | 85 | 23 |

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
