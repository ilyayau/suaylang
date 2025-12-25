# Reviewer Portal (SuayLang)

Welcome, committee reviewers! This portal provides a single, stable entry point for all artifact evaluation, evidence, and reproducibility tasks.

## Quick Links
- [README.md](../README.md) — Project overview, committee narrative
- [docs/EVIDENCE_MAP.md](EVIDENCE_MAP.md) — Claim → metric → artifact map
- [docs/evidence_map.json](evidence_map.json) — Machine-readable evidence map
- [results/README.md](../results/README.md) — Artifact index
- [docs/ARTIFACT_EVALUATION.md](ARTIFACT_EVALUATION.md) — Artifact evaluation guide
- [docs/COMMITTEE_ONEPAGER.md](COMMITTEE_ONEPAGER.md) — 1-page summary
- [docs/TECHREPORT.md](TECHREPORT.md) — Technical report
- [docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) — Threats/limitations
- [docs/NEGATIVE_RESULTS.md](NEGATIVE_RESULTS.md) — What failed / dead ends
- [docs/NONTRIVIALITY.md](NONTRIVIALITY.md) — Why this is not trivial
- [docs/OUT_OF_SCOPE.md](OUT_OF_SCOPE.md) — What is not solved
- [spec/](../spec/) — Versioned specification

## Reproduction Instructions
1. Clone: `git clone https://github.com/ilyayau/suaylang && cd suaylang`
2. Run: `make reproduce-fast` (fast) or `make reproduce-all` (full)
3. Inspect: [results/README.md](../results/README.md) for all evidence

## Evidence Map
- Evidence map (human-readable): docs/EVIDENCE_MAP.md
- Evidence map (machine-readable): docs/evidence_map.json
- Artifact index: results/README.md

## Reviewer UX
- All links are stable and checked (see Makefile: `make check-links`)
- All evidence files are versioned and checksummed (see results/manifest.json)
- All commands are deterministic and documented in [docs/ARTIFACT_EVALUATION.md](ARTIFACT_EVALUATION.md)

## Contact
For questions or issues, see [docs/ARTIFACT_EVALUATION.md](ARTIFACT_EVALUATION.md) or open an issue on GitHub.

---

**This portal is designed for artifact evaluation and committee review. All evidence is discoverable, reproducible, and mapped to claims.**
