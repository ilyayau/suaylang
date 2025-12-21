# SuayLang Technical Report

## Abstract
SuayLang is a research language designed to test the limits of observational equivalence between interpreter and VM backends under a fixed, auditable comparator policy. We present a deterministic, reproducible artifact with a full test harness, coverage metrics, and a robust diagnostics contract. Our evaluation demonstrates that, for a well-defined subset, interpreter and VM executions are indistinguishable on all measured programs, with all results and artifacts versioned and reproducible.

## Research Question & Hypothesis
- **RQ:** Can interpreter and VM executions for a non-trivial language be made observationally equivalent (value, error, stdout) under a fixed comparator policy, across a large, seeded program set?
- **Hypothesis:** For all programs in the test suite, interpreter and VM executions are observationally equivalent under the defined policy.

## Design Rationale
- Expression-oriented control flow enables precise normalization and comparison.
- The language design is intentionally minimal, focusing on features that stress error reporting, control flow, and backend equivalence.
- Novelty: Deterministic artifact pipeline, explicit diagnostics contract, and a comparator policy that is auditable and reproducible.
- Known: Uses established techniques for interpreter/VM design, but applies them to a rigorous artifact evaluation context.

## Semantics & Observational Equivalence
- **Reference Interpreter:** Implements the full language spec, with deterministic error and value reporting.
- **VM:** Bytecode-based backend, sharing the same test suite and comparator policy.
- **Observational Equivalence:** Defined as indistinguishability in value, error (code+span), and stdout, ignoring formatting and non-deterministic output. See [docs/BASELINE.md](BASELINE.md).

## Methodology
- **Test Harness:** All .suay and .py programs in baseline_suite/ are run through both backends.
- **Seeds:** 10 fixed seeds, 5001 programs per seed.
- **Determinism:** All experiments record commit hash, environment, and are fully reproducible.
- **Comparator Policy:** Ignores formatting, non-deterministic output, and external I/O. See [docs/BASELINE.md](BASELINE.md).

## Evaluation
- **Metrics:** Divergences, coverage (AST/opcode), runtime, diagnostics stability.
- **Tables/Figures:**
    - 0 divergences on 5001 programs, 10 seeds.
    - Coverage: 24 AST constructs, 20 opcodes.
    - Benchmarks: 6 programs, median VM runtime 0.138s.
- **Artifacts:** All results in results/, with summary tables in README and [results/README.md](../results/README.md).

## Limitations & Threats to Validity
- See [docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) for detailed discussion.
- Main threats: comparator policy scope, determinism assumptions, coverage gaps, diagnostic contract limitations.

## Related Work
- See [docs/RELATED_WORK.md](RELATED_WORK.md) for full citations and comparison table.
- Comparison table:

| System         | Observational Equivalence | Diagnostics Contract | Determinism | Artifacted |
|----------------|--------------------------|---------------------|-------------|------------|
| SuayLang       | Yes                      | Yes                 | Yes         | Yes        |
| Python         | No                       | Partial             | No          | Yes        |
| OCaml          | No                       | Partial             | Yes         | Yes        |
| Lua            | No                       | No                  | No          | Yes        |

## Reproducibility Checklist
- Hardware: x86_64 Linux, Python 3.12+
- Software: `make`, `pandoc`, `pytest`, `pip install -e .`
- Commands:
    - `make install`
    - `make reproduce` (runs all tests, conformance, diff-test, baseline, ablation, builds PDFs)
    - `make research-pdf` (builds research plan PDF)
- Expected outputs:
    - All results in `results/` (see [results/README.md](../results/README.md))
    - PDFs in `paper/` and `docs/`
- All commands are deterministic and versioned by commit hash.
