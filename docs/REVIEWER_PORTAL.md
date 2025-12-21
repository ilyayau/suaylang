# Reviewer Portal (SuayLang)

Welcome, committee reviewers! This portal provides a single, stable entry point for all artifact evaluation, evidence, and reproducibility tasks.

## Quick Links
- [README.md](../README.md) — Project overview, committee narrative
- [docs/CLAIM_EVIDENCE_MATRIX.md](CLAIM_EVIDENCE_MATRIX.md) — Claim–Evidence matrix
- [results/README.md](../results/README.md) — Artifact index, evidence map
- [docs/ARTIFACT_EVALUATION.md](ARTIFACT_EVALUATION.md) — Artifact evaluation guide
- [docs/COMMITTEE_ONEPAGER.md](COMMITTEE_ONEPAGER.md) — 1-page summary
- [docs/TECH_REPORT.md](TECH_REPORT.md) — Technical report
- [docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) — Threats/limitations

## Reproduction Instructions
1. Clone: `git clone https://github.com/ilyayau/suaylang && cd suaylang`
2. Run: `./scripts/reproduce.sh` (fast) or `./scripts/reproduce.sh --full` (full)
3. Inspect: [results/README.md](../results/README.md) for all evidence

## Evidence Map
- All claims, evidence, and results are mapped in [docs/CLAIM_EVIDENCE_MATRIX.md](CLAIM_EVIDENCE_MATRIX.md)
- All artifact outputs are indexed in [results/README.md](../results/README.md)

## Reviewer UX
- All links are stable and checked (see Makefile: `make check-links`)
- All evidence files are versioned and checksummed (see results/manifest.json)
- All commands are deterministic and documented in [docs/ARTIFACT_EVALUATION.md](ARTIFACT_EVALUATION.md)

## Contact
For questions or issues, see [docs/ARTIFACT_EVALUATION.md](ARTIFACT_EVALUATION.md) or open an issue on GitHub.

---

**This portal is designed for artifact evaluation and committee review. All evidence is discoverable, reproducible, and mapped to claims.**
