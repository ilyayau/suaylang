# Publication plan

This plan targets venues where the contribution is an artifact-grade methodology: a reproducible equivalence protocol with committee-first evidence mapping.

## Target venue types

- **PL / language implementation workshops:** fast feedback on the equivalence protocol and evaluation methodology.
- **Tool/demo tracks:** positioned as an evaluation pipeline + reference implementation + VM.
- **Artifact evaluation tracks (AE):** focuses on reproducibility packaging, integrity metadata, and reviewer UX.

## Submission package (concrete deliverables)

Manuscript layer:
- paper.md (narrative, no hard-coded results)
- docs/TECHREPORT.md (long-form technical report)

Committee layer:
- docs/COMMITTEE_ONEPAGER.md
- docs/REVIEWER_PORTAL.md
- docs/EVIDENCE_MAP.md + docs/evidence_map.json

Artifact layer:
- results/README.md (artifact index)
- results/manifest.json + results/hashes.txt (integrity)
- docs/diagrams/*.svg + docs/diagrams/ascii/*.txt (render-safe diagrams)

## Timeline

Week 1–2:
- Freeze protocol + workflow gates (CI green, coverage threshold enforced)
- Ensure reproduce-fast is ≤5 minutes on CI runners

Week 3–4:
- Expand conformance/differential checks and document falsifiers
- Add independent reproduction receipts mechanism (docs/INDEPENDENT_REPRODUCTIONS.md)

Week 5–6:
- Prepare submission bundle (tagged release + archived artifacts)
- Run external/independent reproduction request and record at least one receipt

## Positioning statement

The novelty is the packaging and falsifiability of the equivalence claim:

- explicit observation policy
- artifact-indexed evidence map
- integrity metadata designed for independent reproduction
