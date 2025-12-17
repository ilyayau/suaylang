# Research protocol (SuayLang v0.1.0)

This document turns the v0.1.0 research claim into a measurable evaluation with fixed tasks and reproducible commands.
The interpreter is the reference semantics; the bytecode VM is evaluated as an alternate execution engine on a defined subset.

## 1) Hypothesis

For a defined, VM-supported subset of SuayLang, expression-based explicit control flow (`dispatch`/`cycle`) enables reproducible observational equivalence testing between the reference interpreter and the bytecode VM, with stable span-based diagnostics.

## 2) Measurements

- **Interpreter↔VM observational equivalence**
  - Corpus conformance: fixed programs with deterministic outcomes.
  - Differential testing: seeded fuzz generation with saved repro cases on divergence.

- **Semantic-construct coverage (qualitative but explicit)**
  - Feature matrix with interpreter/VM support and test pointers: [docs/research/feature_matrix.md](docs/research/feature_matrix.md).

- **Micro-benchmarks (method + recorded sample results)**
  - Median wall-clock time per program (ms) for interpreter and VM.
  - VM instruction count (static count over compiled bytecode, including nested code objects).

- **Diagnostic stability (format + anchoring)**
  - Golden diagnostic snapshots count under `tests/golden/cases/`.

## 3) Tasks (fixed programs)

The fixed task corpus is stored in:

- `evaluation/tasks/`

Included tasks (6 programs):

- `001_fib.suay` (fib, cycle-based)
- `002_map_fold.suay` (map+fold over generated list)
- `003_dispatch_heavy.suay` (dispatch-heavy branching)
- `004_cycle_heavy.suay` (cycle-heavy state evolution)
- `005_mixed_dispatch_cycle.suay` (mixed dispatch+cycle)
- `006_state_machine_workflow.suay` (workflow/state-machine style)

## 4) Victory criteria (quantitative)

These criteria are intentionally conservative and scoped.

1) **Conformance corpus: 0 divergences**
- Runner: `python tools/conformance/run.py`
- Victory: `failures = 0` over the default corpus (`tests/corpus/conformance/*.suay`).

2) **Task corpus: 0 divergences**
- Runner: `python tools/conformance/run.py evaluation/tasks`
- Victory: `failures = 0` over the fixed task set.

3) **Differential fuzz: 0 divergences after N programs**
- Runner: `python -m tools.conformance.fuzz --seed 0 --n 1000`
- Victory: `divergences = 0` for the recorded seed and N.

4) **Coverage table is explicit and non-trivial**
- Artifact: [docs/research/feature_matrix.md](docs/research/feature_matrix.md)
- Victory: at least 12 feature rows show `VM = ✓` and include at least one test pointer (unit/conformance/fuzz/golden).

5) **Diagnostics are regression-checked**
- Artifact: `tests/golden/cases/*.txt`
- Victory: at least 3 golden snapshots exist and pass in CI (lex/parse/runtime represented).

6) **Benchmark reporting is reproducible and comparative**
- Runner: `python benchmarks/run.py evaluation/tasks --iters 200`
- Victory: Markdown table reports interpreter ms, VM ms, ratio, and VM instruction counts for all tasks.
- Optional speed signal (not a requirement): VM has ratio ≥ 1.0 on at least 4/6 tasks in the recorded sample run.

## 5) Protocol (step-by-step)

From repo root:

1) Install (editable) and run unit tests:

- `python -m venv .venv`
- `source .venv/bin/activate` (Windows: `\.venv\Scripts\Activate.ps1`)
- `python -m pip install -U pip`
- `python -m pip install -e ".[dev]"`
- `pytest -q`

2) Conformance (interpreter vs VM):

- Default conformance corpus: `python tools/conformance/run.py`
- Fixed tasks corpus: `python tools/conformance/run.py evaluation/tasks`

3) Differential fuzz (seeded):

- `python -m tools.conformance.fuzz --seed 0 --n 1000`
- If a divergence occurs, inspect saved repro cases under `tools/conformance/fuzz_failures/`.

4) Micro-benchmarks (comparative):

- `python benchmarks/run.py evaluation/tasks --iters 200`

5) Diagnostics stability:

- `pytest -q tests/test_golden_diagnostics.py`

## 6) Threats to validity (short)

- **Subset limitation**: equivalence is claimed only for the VM-supported subset (see [docs/research/semantic_scope.md](docs/research/semantic_scope.md)).
- **Generator bias**: fuzz templates do not uniformly sample all programs; they target termination and VM-supported constructs.
- **Performance noise**: benchmark timings vary with machine load and Python version; only relative comparisons within a run are interpretable.
- **Oracle limitation**: the interpreter is treated as the reference; if the interpreter is wrong, conformance can still pass.
- **Diagnostics scope**: golden snapshots cover a small set of representative errors, not the entire space of messages.
