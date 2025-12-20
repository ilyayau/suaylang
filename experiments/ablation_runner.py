# Ablation Runner

This script runs ablation experiments for SuayLang:
- A) Disables control-flow-as-expr in generator and measures divergence/coverage.
- B) Degrades diagnostics to string-only and measures diagnostic quality metrics.

Outputs:
- results/ablation_raw.json
- results/ablation.md (table)

Usage: python experiments/ablation_runner.py
