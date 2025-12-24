




# SuayLang (Suay Language): Research Artifact for MEXT Review

**Main research claim (1 sentence):** **SuayLang provides two independent executions (reference interpreter and bytecode VM) and a reproducible protocol to test observational equivalence under an explicit observation policy.**

Ultra TL;DR (30 seconds):
- What: a small language + two runtimes (interpreter, VM) + evidence pipeline.
- Why: engineering-style cross-checking as a research method (two implementations, one spec).
- Evidence is file-based: every claim links to a concrete artifact under results/.
- Reproduce (canonical): `make reproduce-all` (or `bash ./scripts/reproduce.sh` for the scripted path).
- If results diverge, see: docs/REPRODUCIBILITY.md ("If results diverge" section).

Evidence map (click → file → command):
- 30 seconds: this page (claim + command + evidence map)
- 7 minutes: [docs/REVIEWER_PORTAL.md](docs/REVIEWER_PORTAL.md) → [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) → [results/README.md](results/README.md)
- 15 minutes: [docs/TECHREPORT.md](docs/TECHREPORT.md) + [docs/THREATS_TO_VALIDITY.md](docs/THREATS_TO_VALIDITY.md) + [docs/LIMITATIONS.md](docs/LIMITATIONS.md)
- Claim↔evidence table: [docs/CLAIM_EVIDENCE_MATRIX.md](docs/CLAIM_EVIDENCE_MATRIX.md)

Quickstart (≤8 lines):
```sh
python3.12 -m venv .venv && . .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
make reproduce-all
ls -la results/
```

Diagrams (pre-rendered SVG; no Mermaid dependency):

![Architecture overview (interpreter + VM + evidence pipeline)](docs/diagrams/architecture_overview.svg)

![Equivalence / evidence flow (claim → protocol → artifacts → hashes)](docs/diagrams/equivalence_flow.svg)

Primary artifacts (index + hashes):

| Claim surface | Where to look | What you should see | Reproduce |
|---|---|---|---|
| Equivalence protocol | results/README.md | an artifact index + generation receipt | `make reproduce-all` |
| Baseline suite timings | results/baseline.md | table regenerated on your machine | `make baseline` |
| Microbench example + plot | benchmarks/results.md and docs/plots/microbench_relative.png | "example run" table + a relative plot | `make plot-microbench` |
| Artifact hashes | results/manifest.json and results/hashes.txt | SHA-256 per artifact | `make hashes` |

If you only read one page: docs/COMMITTEE_ONEPAGER.md

Entry hub for reviewers: [docs/REVIEWER_PORTAL.md](docs/REVIEWER_PORTAL.md)

How to cite: CITATION.cff
