# Research Plan (SuayLang as a language/semantics artifact)

## 1) Field of Study

Programming Languages (PL) / Language Semantics / Systems

## 2) Research Objective

Produce a small, reproducible research artifact in which a reference interpreter and a bytecode VM can be validated for observational equivalence on a documented subset of a language with explicit, expression-level control flow.

## 3) Research Methodology

SuayLang is used as a combined platform for:

- **Language design experiment**
  - The language emphasizes explicit control constructs (`dispatch` and `cycle`) and explicit state change (`←` binding vs `⇐` mutation).
  - Semantics are scoped and documented for evaluation (see [docs/research/semantic_scope.md](docs/research/semantic_scope.md)).

- **Interpreter + VM validation platform**
  - The reference interpreter defines baseline behavior.
  - The bytecode VM is treated as an alternative execution strategy for a supported subset.
  - Validation uses:
    - differential testing (seeded fuzzing and a small conformance corpus), and
    - micro-benchmarks that compare interpreter vs VM only.

Concrete evaluation artifacts already present in the repository:

- Differential testing report: [docs/research/differential_testing.md](docs/research/differential_testing.md)
- Fuzz runner: [tools/conformance/fuzz_runner.py](tools/conformance/fuzz_runner.py)
- Corpus runner: [tools/conformance/run.py](tools/conformance/run.py)
- Benchmark results: [benchmarks/results.md](benchmarks/results.md)

## 4) Research Schedule (6–12 months)

Month 1–2:
- Freeze evaluation scope and claims for v0.1.
- Maintain a strict separation between “language semantics” and “tooling/implementation details”.
- Deliverable: updated scope statement if needed; keep claims aligned with artifacts.

Month 3–4:
- Strengthen conformance evidence without expanding language features:
  - extend the conformance corpus with additional small, deterministic programs (still within the VM-supported subset),
  - add regression cases if any discrepancies are discovered.
- Deliverable: expanded corpus and clear failure reproduction procedure.

Month 5–6:
- Strengthen differential fuzz evidence:
  - run multiple seeds and report $N$ programs per seed,
  - track and document any divergences and fixes (if found).
- Deliverable: updated differential testing report with numeric totals and reproduction commands.

Month 7–9:
- Improve benchmark methodology reporting (not performance claims):
  - verify benchmark programs are identical across backends,
  - report median timing and VM instruction count,
  - document expected variability and limitations.
- Deliverable: stable benchmark table and reproducibility notes.

Month 10–12:
- Assemble the evaluation write-up:
  - single-source documents suitable for conversion to a PDF,
  - a short “core research claim” page,
  - related work bullets focused on design relevance.
- Deliverable: complete, review-ready document set and a reproducible evaluation checklist.

## 5) Expected Results

- **Validated execution equivalence** (for a clearly documented VM-supported subset), supported by reproducible differential testing.
- **Reproducible research artifact**: a repository with scoped semantics, tests, and benchmark methodology that can be rerun by third parties.
- **Publishable evaluation package**: concise documents and numeric results suitable for academic review, without broad or inflated claims.
