# Reviewer Path (15 minutes)

This path is designed for a skeptical reviewer to answer, quickly and with evidence:

- What is the research question?
- What would falsify it?
- What did we measure and what did we observe?

All commands below are copy-paste from repo root.

## Minute 0–3: Read the claim

1) Research core (RQ/Hypotheses/Metrics/Falsification):

- [docs/research/RESEARCH_CORE.md](../research/RESEARCH_CORE.md)

2) Scope control (what is intentionally not claimed):

- [docs/SCOPE.md](../SCOPE.md)

3) Supported subset for equivalence (what the VM is expected to cover):

- [docs/spec/supported_subset.md](../spec/supported_subset.md)

## Minute 3–8: Run the evidence-producing commands

### 1) Unit tests (sanity + regression)

```sh
python -m pip install -e ".[dev]"
pytest -q
```

Evidence:

- Pytest summary shows baseline regressions are green.

### 2) Conformance: interpreter ↔ VM (expanded fixed corpus)

```sh
python tools/conformance/run.py conformance/corpus
```

Evidence:

- Prints a single summary line: `conformance: OK files=... divergences=0 ...`.
- Counterexamples (if any) are printed with interpreter/VM observations.

### 3) Differential fuzzing: interpreter ↔ VM (seeded, deterministic)

```sh
python -m tools.conformance.fuzz --seed 0 --n 1000
```

Evidence:

- Prints `fuzz: seed=0 n=1000 divergences=...`.
- (When enabled) raw run summaries are written under `data/raw/fuzz_runs/`.

### 4) H2 one-line summary (M/N/divergences/subset size)

```sh
python tools/research/h2_eval.py
```

Evidence:

- Prints: `H2: corpus M=... fuzz N=... divergences=... subset_constructs X=...`.

### 5) Demo (non-toy workflow state machine)

```sh
suay run demos/workflow_state_machine/main.suay
```

Evidence:

- Demonstrates `dispatch` + `cycle` as explicit workflow/state machine.

## Minute 8–12: Check the supporting tables

- H2 results snapshot: [docs/research/H2_results.md](../research/H2_results.md)
- Coverage matrix: [docs/research/coverage_matrix.md](../research/coverage_matrix.md)
- Differential testing report: [docs/research/differential_testing.md](../research/differential_testing.md)
- Readability proxy notes (H1-style evidence): [docs/research/READABILITY_NOTES.md](../research/READABILITY_NOTES.md)
- Diagnostics quality: [docs/research/DIAGNOSTICS_QUALITY.md](../research/DIAGNOSTICS_QUALITY.md)

## Minute 12–15: Read the paper-style artifact

- Paper kit entry: [docs/paper/suaylang_paper.md](../paper/suaylang_paper.md)
