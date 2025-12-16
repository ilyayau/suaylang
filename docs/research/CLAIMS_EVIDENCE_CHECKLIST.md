# Claims → evidence checklist (SuayLang v0.1 research artifact)

This is a reviewer-facing map from research claims to concrete evidence in the repository.

## H1: expression-based, pattern-driven control improves composability/local reasoning

Evidence:
- Hypothesis + threats: docs/research/HYPOTHESIS.md
- Micro-evaluation rubric + tasks: docs/research/MICRO_EVAL.md
- Task sources (SuayLang): docs/research/tasks/*.suay
- Task baselines (Python): docs/research/tasks/baselines/*.py
- Metric computation: scripts/micro_eval.py

## C2/C3: predictability and VM mapping

Evidence:
- Semantic contract (v0.1): docs/LANGUAGE_CONTRACT_v0.1.md
- Bytecode documentation: docs/BYTECODE.md
- Conformance definition + coverage statement: docs/research/CONFORMANCE.md
- Differential runner + corpus:
  - scripts/conformance.py
  - tests/corpus/conformance/*.suay
  - tests/test_conformance_corpus.py
  - tests/test_conformance_fuzz.py

## VM justification: relative performance on control-flow-heavy micro-benchmarks

Evidence:
- Benchmark programs: benchmarks/*.suay
- Benchmark runner: scripts/bench_micro.py
- Results discussion: docs/research/BENCHMARKS_v0.1.md

## Unicode syntax as a research variable

Evidence:
- Design trade-off discussion: docs/research/UNICODE_VARIABLE.md
- Accessibility redesign discussion (future experiment): docs/ACCESSIBILITY_REDESIGN.md

## Reproducibility / 15-minute reviewer path

- Install + quick checks: docs/QUICKSTART.md and RELEASE.md
- Minimal “trust run”:
  - `pytest -q`
  - `python scripts/smoke.py`
  - `python scripts/conformance.py`
  - `python scripts/bench_micro.py`

Primary paper text:
- docs/research/SUAYLANG_EVAL_PAPER_v0.1.md
