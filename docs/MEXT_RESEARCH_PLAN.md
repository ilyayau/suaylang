# Research Plan (SuayLang)

## 1. Field of Study

Programming Languages / Language Semantics / Software Systems

## 2. Research Topic / Title

Validating interpreter–VM observational equivalence for a small language with explicit, expression-level control flow

## 3. Background & Motivation (2–3 sentences)

When a language has both a reference interpreter and an alternate execution engine (e.g., a bytecode VM), semantic drift can occur without being obvious to users. A small language with a compact semantic surface is suitable for controlled, repeatable evaluation of equivalence. SuayLang provides explicit control flow (`dispatch`/`cycle`) and span-based diagnostics, making it a practical artifact for measurable backend-comparison experiments.

## 4. Research Objective (1–2 bullet points)

- Define a conservative, test-backed equivalence claim for a VM-supported subset of SuayLang.
- Measure interpreter–VM agreement using a fixed corpus and seeded differential testing.

## 5. Methodology

- **Implementations**: reference interpreter + bytecode compiler/VM (alternate execution).
- **Differential testing**: conformance corpus (`python tools/conformance/run.py`) and seeded fuzzing (`python -m tools.conformance.fuzz --seed S --n N`).
- **Benchmarks (method only)**: micro-benchmarks compare interpreter vs VM on identical programs (see [benchmarks/results.md](benchmarks/results.md)).
- **Documentation**: scope and feature coverage are documented (see [docs/research/semantic_scope.md](docs/research/semantic_scope.md) and [docs/research/feature_matrix.md](docs/research/feature_matrix.md)).

## 6. Research Schedule (6–12 months)

- Months 1–2: freeze subset/scope claim; ensure all scope links and commands are reproducible.
- Months 3–4: extend conformance corpus within scope; add regressions for any discovered mismatches.
- Months 5–6: run multiple seeds with reported N; record divergences and fixes (if any).
- Months 7–9: stabilize benchmark methodology reporting (median, instruction count, variability notes).
- Months 10–12: finalize a short evaluation packet (claim + scope + results) and a reviewer checklist.

## 7. Expected Results / Contribution (conservative, measurable)

- A documented subset and an explicit observation policy for interpreter–VM equivalence.
- Reported totals of programs tested (corpus size + fuzz N) and divergences observed per seed.
- A stable, rerunnable evaluation artifact (tests + conformance + fuzz + benchmark methodology) suitable for independent reruns.

## 8. Reproducibility & Dissemination

- Open-source repository with pinned commands and runnable artifacts.
- Primary evidence artifacts: tests (`pytest`), conformance runner, fuzz runner, and benchmark scripts/results.
