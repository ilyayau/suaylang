# Negative results

This document records failures, dead ends, and approaches that did not work (or were intentionally rejected) during the work on SuayLang as a research artifact.
It exists to reduce hindsight bias and to help reviewers understand design tradeoffs.

## 1) Mermaid-in-README as a rendering dependency

What was tried:
- Embedding Mermaid diagrams directly in README.

Why it failed:
- GitHub rendering is context-dependent; Mermaid blocks can be disabled or behave inconsistently.
- Committee review requires that the README renders identically in standard GitHub viewers.

What replaced it:
- Pre-rendered SVG diagrams under docs/diagrams/*.svg
- ASCII fallbacks under docs/diagrams/ascii/*.txt
- Mermaid sources (optional) under docs/diagrams/src/*.mmd

## 2) Overly strict Python version gating in packaging

What was tried:
- Tight `requires-python` bounds that excluded Python 3.13.

Why it failed:
- Clean environments (including reviewer machines) may have Python 3.13 installed.
- Editable install fails immediately even though the project is compatible.

What replaced it:
- Supported range is declared as `>=3.12,<3.14`.
- CI is pinned to Python 3.12.8 to keep the gate stable.

## 3) “Coverage plot” derived from unrelated counts

What was tried:
- A plot labeled as coverage derived from benchmark count.

Why it failed:
- It conflates the number of benchmark programs with language-feature coverage.
- It is not a meaningful coverage metric.

What replaced it:
- Coverage plots are now derived from results/coverage.json (corpus coverage pipeline output).

## 4) Placeholder-heavy artifacts

What was tried:
- Scaffold documents that referenced future results without generated artifacts.

Why it failed:
- Committee review expects concrete artifacts or explicit removal.

What replaced it:
- All numeric results live in generated artifacts under results/.
- Docs link to artifacts rather than repeating numbers.

## 5) Multiple workflows that do the same thing

What was tried:
- Separate CI and artifact evaluation workflows.

Why it failed:
- Drift between workflows increases the probability that the “reviewer path” diverges from CI.

What replaced it:
- One canonical CI workflow that runs reproduce-fast on PR/push and reproduce-all on nightly/dispatch.

See also:
- docs/THREATS_TO_VALIDITY.md
- docs/REPRODUCIBILITY.md
