# Independent Reproduction Logs

This folder is a placeholder for independent reproduction receipts.

Goal: allow a reviewer (or a third party) to record a minimal, auditable reproduction attempt without editing prose documents.

## How to use

1) Run the canonical pipeline:

```sh
make reproduce-all
```

2) Copy the template and fill it in:

- receipt_template.md

3) Attach the integrity metadata from your run:

- results/manifest.json
- results/hashes.txt
