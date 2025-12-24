# SuayLang — Research Artifact (Interpreter + Bytecode VM)

Ultra TL;DR (30 seconds):
- What: a small language + two runtimes (reference interpreter and bytecode VM).
- Why: cross-checking two implementations as a research method.
- Evidence is file-based and reproducible: artifacts live under results/ and docs/plots/.
- Reproduce the full artifact pipeline: `make reproduce-all`.
- If results diverge: see docs/REPRODUCIBILITY.md.

**Main research claim:** **Interpreter and VM are observationally equivalent under an explicit observation policy, evaluated by a deterministic evidence pipeline.**

Evidence map (click → read → reproduce):
- 30 seconds: [docs/REVIEWER_PORTAL.md](docs/REVIEWER_PORTAL.md)
- 7 minutes: [docs/COMMITTEE_ONEPAGER.md](docs/COMMITTEE_ONEPAGER.md) → [docs/EVIDENCE_MAP.md](docs/EVIDENCE_MAP.md) → [results/README.md](results/README.md)
- 15 minutes: [docs/TECHREPORT.md](docs/TECHREPORT.md) and `make reproduce-all`

15-minute path (commands):
```sh
python3.12 -m venv .venv && . .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev,plots]"
make reproduce-all
python -m pytest -q
```

Rendering note: README contains no Mermaid blocks. Diagrams are committed SVGs:
- [docs/diagrams/architecture_overview.svg](docs/diagrams/architecture_overview.svg)
- [docs/diagrams/equivalence_flow.svg](docs/diagrams/equivalence_flow.svg)
- [docs/diagrams/pipeline.svg](docs/diagrams/pipeline.svg)

How to cite:
- [CITATION.cff](CITATION.cff)
- [docs/citations.bib](docs/citations.bib)

Everything beyond this first screen is in docs/.
