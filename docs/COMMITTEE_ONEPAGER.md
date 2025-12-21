
# SuayLang: Committee One-Pager

## Research Impact
SuayLang sets a new standard for artifact evaluation in programming languages research by delivering bit-for-bit equivalence between interpreter and VM backends, under a transparent, reviewer-auditable observation policy. All claims are directly evidenced, reproducible, and falsifiable by construction.

## Main Claim
Interpreter and VM executions for SuayLang are observationally equivalent under a fixed, formal observation policy ([see policy](OBSERVATION_POLICY.md)), evidenced by deterministic, reproducible experiments.

## Evidence & Results
- **Diff test:** 0 divergences, 5001 programs, 10 seeds ([diff_report.md](../results/diff_report.md))
- **Baseline:** 5 programs, timings ([baseline.md](../results/baseline.md))
- **Coverage:** 24 AST, 20 opcodes ([coverage.md](../results/coverage.md))
- **Diagnostics contract:** ([golden_diagnostics.md](../results/golden_diagnostics.md))
- **Ablation/mutation:** ([ablation.md](../results/ablation.md), [mutation_catches.md](../results/mutation_catches.md))
- **Manifest/environment:** ([manifest.json](../results/manifest.json), [environment.json](../results/environment.json))

## Observation Policy
See [docs/OBSERVATION_POLICY.md](OBSERVATION_POLICY.md) for the formal definition of what is compared, what is ignored, and how the claim can be falsified. This policy is the contract for all equivalence evidence.

## Reviewer Experience
- **Reproduce (fast):** `bash ./scripts/reproduce.sh`
- **Reproduce (full):** `bash ./scripts/reproduce.sh --full`
- **Artifact index:** [results/README.md](../results/README.md)
- **Reviewer attack questions:** [REVIEWER_ATTACKS.md](REVIEWER_ATTACKS.md)

## Limitations & Threats
- Only tested on Linux, Python 3.12.x
- v0.1, single-threaded, no concurrency/JIT/optimizer
- Comparator ignores formatting, possible false negatives ([see policy](OBSERVATION_POLICY.md))
- IDE plugin (vscode-extension/) is WIP and not part of evaluated claims for v0.1

## How to Falsify
See [OBSERVATION_POLICY.md](OBSERVATION_POLICY.md#how-to-falsify-this-claim) for explicit falsifiability criteria. Any divergence in value, error, or stdout between interpreter and VM falsifies the main claim and will be caught by the test harness.
