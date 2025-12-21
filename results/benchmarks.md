# Benchmarks (SuayLang)

Backed by raw JSON in `results/bench_raw.json`.

- commit: `4234c44ddc148f009e738402c684135de7e2e497`
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
| 01_fibonacci.suay | 2.556/2.587 | 0.324/0.349 | 19784.713/19926.958 | 15496.740/15597.528 | 1.28 | 104 | 12 |
| 02_dispatch_heavy.suay | 1.783/1.820 | 0.280/0.284 | 18.381/19.025 | 24.129/24.270 | 0.76 | 180 | 14 |
| 03_cycle_state_machine.suay | 1.172/1.230 | 0.154/0.158 | 188.844/189.670 | 175.878/176.506 | 1.07 | 93 | 9 |
| 04_map_fold.suay | 0.844/0.964 | 0.089/0.096 | 0.340/0.347 | 0.285/0.423 | 1.19 | 54 | 46 |
| 05_string_and_collections.suay | 1.670/1.694 | 0.194/0.196 | 10.586/10.887 | 8.533/8.583 | 1.24 | 111 | 40 |
| 06_module_access.suay | 1.207/1.244 | 0.140/0.157 | 37.931/39.917 | 32.520/32.840 | 1.17 | 85 | 23 |

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
