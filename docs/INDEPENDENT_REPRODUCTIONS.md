# Independent reproductions

This file collects independent reproduction receipts.

## How to add a receipt

1) Copy the template:
- results/independent_reproduction/receipt_template.md

2) Fill it out and save as a new file under:
- results/independent_reproduction/YYYY-MM-DD_<name_or_org>.md

3) Attach (or include) the hashes you observed:
- results/manifest.json
- results/hashes.txt

## Logged reproductions

### 2025-12-25 — Automated CI reproduction (GitHub Actions)

- Source of truth: CI workflow runs `make reproduce-fast` on PR/push and `make reproduce-all` on nightly/dispatch.
- Evidence artifacts: uploaded workflow artifacts include `results/`, `docs/plots/`, and `docs/diagrams/`.
- Receipt format: when an external reproducer runs locally, they should add a receipt file under results/independent_reproduction/.
