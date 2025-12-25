SuayLang is a research artifact that evaluates observational equivalence between a reference interpreter and a bytecode VM for a small control‑flow language via a deterministic, file-based evidence pipeline.

| claim | evidence | artifact |
|---|---|---|
| Interpreter and VM are observationally equivalent for the shipped corpora under an explicit observation policy | Read: [docs/OBSERVATION_POLICY.md](docs/OBSERVATION_POLICY.md); Reproduce: `make reproduce-all` | [results/diff_report.md](results/diff_report.md) (+ [results/diff_report.json](results/diff_report.json)) |
| Baseline timings are computed reproducibly (per machine) for paired .py/.suay programs | Read: [experiments/baseline_runner.py](experiments/baseline_runner.py); Reproduce: `make baseline` | [results/baseline.md](results/baseline.md) (+ [results/baseline_raw.json](results/baseline_raw.json)) |
| Committee-facing plots are generated from artifacts and pre-rendered (no Mermaid required) | Read: [tools/plot_results.py](tools/plot_results.py); Reproduce: `make plots-fast` (or `make plots`) | [docs/plots/interp_vs_vm.png](docs/plots/interp_vs_vm.png) (+ [docs/diagrams/pipeline.svg](docs/diagrams/pipeline.svg), [docs/diagrams/ascii/pipeline.txt](docs/diagrams/ascii/pipeline.txt)) |

# SuayLang

Ultra TL;DR (30 seconds):
- Two independent executions: interpreter + bytecode VM.
- Equivalence is defined by an explicit observation policy (what counts as “same”).
- Evidence is generated into `results/` and integrity-checked (manifest + hashes).
- README renders without Mermaid; diagrams are committed SVG + ASCII fallback.
- One entrypoint for reviewers: [docs/REVIEWER_PORTAL.md](docs/REVIEWER_PORTAL.md).

## Research question (yes/no)
RQ: **Do the interpreter and VM produce the same observable behavior for the shipped test corpora under the declared observation policy?**

## Falsifiable hypothesis + falsifier
H: **For every program in the shipped corpora, interpreter and VM observations are equal after normalization defined in the observation policy.**

Falsifier: **`make reproduce-all` produces a non-empty counterexample (a program where observations differ) recorded in `results/diff_report.md`/`results/diff_report.json`.**

## Novelty (relative to approach classes)
This project’s novelty is not a new testing primitive; it is a committee-first packaging of an equivalence claim relative to:
- Differential testing (e.g., compiler validation by cross-execution): adds an explicit observation policy + artifact-indexed evidence.
- Property-based testing (e.g., QuickCheck-style generation): adds deterministic seed logging + a reproducible, file-based evidence pipeline.
- Artifact evaluation norms: integrates integrity metadata (`results/manifest.json`, `results/hashes.txt`) as first-class outputs.

## Related work (categorized, with limitations)
- Differential testing / compiler validation: powerful for finding divergences; limitation: can miss shared-oracle bugs and unexercised behaviors.
- Property-based testing: broad input coverage with shrinking; limitation: generator bias and incomplete language subset can create false confidence.
- Reproducible research / AE norms: improves repeatability; limitation: reproducibility does not imply correctness of the underlying claim.

## What this project does NOT solve
- Proving semantic equivalence for all programs (this is evidence-based, corpus-scoped).
- Detecting every class of shared logic bug between implementations.
- Providing a full production language stack (stdlib, concurrency, macros, etc.).

## Quickstart (≤10 lines)
```sh
python3.12 -m venv .venv && . .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev,plots]"
make reproduce-fast
python -m pytest --cov=suaylang
```

## 15-minute path
```sh
python3.12 -m venv .venv && . .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev,plots]"
make reproduce-all
```

## Required reviewer docs
- Portal: [docs/REVIEWER_PORTAL.md](docs/REVIEWER_PORTAL.md)
- Committee one-pager: [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md)
- Evidence map: [docs/EVIDENCE_MAP.md](docs/EVIDENCE_MAP.md) (+ [docs/evidence_map.json](docs/evidence_map.json))
- Negative results: [docs/NEGATIVE_RESULTS.md](docs/NEGATIVE_RESULTS.md)
- Nontriviality: [docs/NONTRIVIALITY.md](docs/NONTRIVIALITY.md)
- Publication plan: [docs/PUBLICATION_PLAN.md](docs/PUBLICATION_PLAN.md)
- Specification: [spec/](spec/)
