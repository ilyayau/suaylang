# SuayLang: Technical Report

## Abstract
This report presents SuayLang, a research artifact for evaluating interpreter–VM observational equivalence under a fixed, auditable observation policy. All claims are evidenced by deterministic, reproducible experiments.

## Introduction
Backend equivalence is a core challenge in language implementation. SuayLang provides a reproducible, committee-grade artifact for evaluating interpreter and VM equivalence, diagnostics contracts, and baseline/ablation.

## Research Questions
- RQ1: Are interpreter and VM executions observationally equivalent on the full test suite?
- RQ2: Is the diagnostics contract stable and enforced?
- RQ3: Are all results reproducible with fixed seeds and environment metadata?

## Method
- Deterministic, multi-seed differential testing
- Golden diagnostics contract
- Coverage and ablation studies
- All results are saved as artifacts and reproducible by `make reproduce`

## Formal Core Summary
See [docs/FORMAL_CORE.md](../docs/FORMAL_CORE.md)

## Evaluation
See [results/README.md](../results/README.md) for all metrics and evidence.

## Threats to Validity
See [docs/THREATS_TO_VALIDITY.md](../docs/THREATS_TO_VALIDITY.md)

## Related Work
See [docs/RELATED_WORK.md](../docs/RELATED_WORK.md)

## Limitations
See [docs/LIMITATIONS.md](../docs/LIMITATIONS.md)

## Conclusion
SuayLang demonstrates a reproducible, committee-grade approach to backend equivalence and diagnostics contract, suitable as a foundation for graduate-level research in PL/compilers.
