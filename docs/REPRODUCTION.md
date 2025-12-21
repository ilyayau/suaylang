# Reproduction Instructions

## One-Command Reproduction

Run:

```
make reproduce
```

This will:
- Run all tests, conformance, diff-test (CI subset), baseline, ablation
- Build all PDFs
- Save all results to results/ and paper/
- Record environment metadata (OS, Python version, commit hash, seeds)

## Output Artifacts
- results/*.md, results/*.json
- see docs/TECH_REPORT.md (PDF: run `make tech-report-pdf`)
- results/manifest.json (contains seeds, commit hash, environment)
