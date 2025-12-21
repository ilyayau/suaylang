# Reviewer Checklist

## Claims → Evidence
- [ ] Thesis claim matches artifact ([docs/THESIS_CLAIM.md](THESIS_CLAIM.md))
- [ ] Formal summary is present ([docs/FORMAL_SUMMARY_1PAGE.md](FORMAL_SUMMARY_1PAGE.md))
- [ ] Falsification scenarios are explicit ([docs/FALSIFICATION.md](FALSIFICATION.md))
- [ ] All results are reproducible ([docs/INDEPENDENT_REPRODUCTION.md](INDEPENDENT_REPRODUCTION.md))

## Reproducibility
- [ ] `make research` and `make tr` run without error
- [ ] All results/ and paper/TR-2025-01.pdf are generated
- [ ] Manifest includes commit, env, seeds ([results/manifest.json](../results/manifest.json))

## Equivalence Testing
- [ ] Differential test: 0 divergences ([results/diff_report.md](../results/diff_report.md))
- [ ] Coverage by construct ([results/coverage_by_construct.md](../results/coverage_by_construct.md))

## Diagnostics Contract
- [ ] Golden diagnostics contract ([results/golden_diagnostics.md](../results/golden_diagnostics.md))
- [ ] Error code stability ([docs/FORMAL_SUMMARY_1PAGE.md](FORMAL_SUMMARY_1PAGE.md))

## Benchmarks
- [ ] Benchmarks and baseline ([results/benchmarks.md](../results/benchmarks.md), [results/baseline.md](../results/baseline.md))

## Baselines
- [ ] Python baseline is real ([results/baseline.md](../results/baseline.md))
- [ ] Ablation study is present ([results/ablation.md](../results/ablation.md))

## Threats / Limitations
- [ ] Threats to validity ([docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md))
- [ ] Non-goals and limitations ([docs/NON_GOALS.md](NON_GOALS.md))
- [ ] Known imperfection is documented ([docs/KNOWN_INTENTIONAL_IMPERFECTION.md](KNOWN_INTENTIONAL_IMPERFECTION.md))
