# SuayLang Technical Report

## Abstract
SuayLang is a research language designed to study observational equivalence between two independent executions: a reference interpreter and a bytecode VM, under a fixed and auditable observation policy. The artifact is structured so that each claim maps to versioned evidence files and a reproduction command, rather than relying on narrative-only assertions.

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
- **Observational Equivalence:** Defined as indistinguishability in value, error (code+span), and stdout, subject to explicit exclusions. See [docs/OBSERVATION_POLICY.md](OBSERVATION_POLICY.md).

## Methodology
- **Test Harness:** All .suay and .py programs in baseline_suite/ are run through both backends.
- **Seeds:** Seeds and corpus sizes are recorded in the generated evidence artifacts (do not hard-code them here).
- **Determinism:** Experiments record commit hash and environment metadata in results/manifest.json.
- **Comparator / Observation Policy:** See docs/OBSERVATION_POLICY.md.

## Evaluation
- **Metrics:** Divergences, coverage (AST/opcode), runtime, diagnostics stability.
- **Tables/Figures:**
    - All concrete values are read from artifacts under results/ and docs/plots/.
- **Artifacts:** See results/README.md for the artifact index and docs/CLAIM_EVIDENCE_MATRIX.md for claim↔evidence mapping.

## Limitations & Threats to Validity
- See [docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) for detailed discussion.
- Main threats: comparator policy scope, determinism assumptions, coverage gaps, diagnostic contract limitations.

## Related Work
- See [docs/RELATED_WORK.md](RELATED_WORK.md) for full citations and comparison table.

Comparative claims are intentionally not asserted in this report; committee reviewers should treat this as an artifact report, not a survey.

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
