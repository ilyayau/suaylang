# H2 results: interpreter↔VM observational equivalence

H2 statement (see [docs/research/RESEARCH_CORE.md](RESEARCH_CORE.md)):

> Interpreter and bytecode VM can be made observationally equivalent on a defined subset, and equivalence can be validated automatically.

## Supported subset

The equivalence claim is limited to the VM-supported subset defined in:

- [docs/spec/supported_subset.md](../spec/supported_subset.md)

Subset construct categories (expression-level): **X = 14** (counted from the subset spec).

## Evaluation pipeline (reproducible)

Commands (from repo root):

```sh
pytest -q

python tools/conformance/run.py
python tools/conformance/run.py evaluation/tasks
python tools/conformance/run.py conformance/corpus

python -m tools.conformance.fuzz --seed 0 --n 1000 --raw

python tools/research/h2_eval.py --seed 0 --n 1000
```

## Numeric summary (current snapshot)

- Corpus size (baseline conformance + fixed tasks): **M = 10** programs
- Fuzz: **seed=0, N = 1000**
- Divergences: **0**
- Bugs found & fixed while reaching divergences=0: **K = 0** (no divergences observed in this snapshot)

One-line summary output:

```text
H2: corpus M=10 fuzz N=1000 divergences=0 bugs_fixed K=0 subset_constructs X=14
```

Raw evidence artifacts:

- Raw fuzz logs: `data/raw/fuzz_runs/seed_0_n_1000.jsonl`
- Coverage matrix: [docs/research/coverage_matrix.md](coverage_matrix.md)
