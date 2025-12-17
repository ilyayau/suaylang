# Results snapshot (SuayLang v0.1.0)

This file records a reproducible “snapshot” of the v0.1.0 evaluation outputs.
Numbers below were collected on the local developer machine; timings are machine-dependent.

## How to reproduce (exact commands)

From repo root (after installing in a venv):

- Conformance (fixed corpus): `python tools/conformance/run.py`
- Conformance (fixed tasks): `python tools/conformance/run.py evaluation/tasks`
- Differential fuzz: `python -m tools.conformance.fuzz --seed 0 --n 1000`
- Micro-benchmarks (Markdown table): `python benchmarks/run.py evaluation/tasks --iters 200`
- Golden diagnostics regression: `pytest -q tests/test_golden_diagnostics.py`

## A) Interpreter↔VM equivalence results

### Conformance corpora

| Corpus | Files | Divergences | Command |
|---|---:|---:|---|
| `tests/corpus/conformance/` | 4 | 0 | `python tools/conformance/run.py` |
| `evaluation/tasks/` | 6 | 0 | `python tools/conformance/run.py evaluation/tasks` |

Recorded outputs:

```text
conformance: OK files=4 divergences=0 pass=4 fail=0
conformance: OK files=6 divergences=0 pass=6 fail=0
```

### Differential fuzz (seeded)

| Seed | N programs | Divergences | ok | runtime | lex | parse | internal |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1000 | 0 | 662 | 338 | 0 | 0 | 0 |

Recorded output:

```text
fuzz: seed=0 n=1000 divergences=0 ok=662 runtime=338 lex=0 parse=0 internal=0
```

## B) Micro-benchmarks (interpreter vs VM)

Method:

- Timing uses `time.perf_counter()` and reports the **median** over `--iters` runs, after warm-up.
- The VM instruction count is the number of compiled bytecode instructions (including nested code objects).

Table (recorded run):

| Program | Interpreter (ms) | VM (ms) | Relative (interp/vm) | VM instr |
|---|---:|---:|---:|---:|
| evaluation/tasks/001_fib.suay | 0.780 | 0.691 | 1.13 | 60 |
| evaluation/tasks/002_map_fold.suay | 44.162 | 36.886 | 1.20 | 81 |
| evaluation/tasks/003_dispatch_heavy.suay | 84.468 | 69.208 | 1.22 | 89 |
| evaluation/tasks/004_cycle_heavy.suay | 133.857 | 116.203 | 1.15 | 58 |
| evaluation/tasks/005_mixed_dispatch_cycle.suay | 108.137 | 93.089 | 1.16 | 83 |
| evaluation/tasks/006_state_machine_workflow.suay | 0.348 | 0.359 | 0.97 | 162 |

Interpretation:

- In this run, the VM is faster on 5/6 tasks and slightly slower on the workflow task.
- Instruction counts provide a static proxy for “work done” by the VM, but do not predict runtime alone.

## C) Diagnostic stability (golden snapshots)

| Artifact | Count | Location |
|---|---:|---|
| Golden diagnostic snapshots (`*.txt`) | 3 | `tests/golden/cases/` |

## Conclusions (conservative)

- Interpreter and VM observations agree for the fixed conformance corpus (4 programs) and the fixed task set (6 programs).
- Differential fuzzing at seed 0 and N=1000 produced 0 divergences under the current observation policy.
- Benchmark reporting is comparative and reproducible (median timings + VM instruction counts), but machine-dependent.

## Limitations

- Equivalence is scoped to the VM-supported subset; interpreter-only features (e.g., `link` modules) are excluded.
- The fuzz generator uses bounded templates and is not an unbiased sample of all programs.
- Golden diagnostics currently cover a small number of representative cases and should be expanded as new error modes are stabilized.
