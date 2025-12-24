# Execution plan (Phase 6)

As of 2025-12-24, this turns the broad backlog into an executable, reviewer-facing plan.
Scope is **research-grade evidence + reproducibility + reviewer UX**, not new language features.

## 10 buckets (workstreams)

1) **CI + clean-runner determinism**
- DoD: CI stays green; pinned toolchain; reproducible pipeline runs from a clean checkout.

2) **Repro pipeline integrity (artifacts + hashes)**
- DoD: `results/manifest.json` and hash files are validated by a dedicated check; failures are actionable.

3) **Evidence map alignment (claims → artifacts)**
- DoD: every top-level claim in docs has a corresponding generated artifact and a reproduce command.

4) **Interpreter ↔ VM conformance**
- DoD: corpus growth is measurable; failures are triaged with minimized repro cases; diagnostics match contract.

5) **Diagnostics contract + error codes**
- DoD: error-code taxonomy is stable; tests assert spans and codes; documentation stays consistent.

6) **Benchmark suite hygiene**
- DoD: benchmark programs are documented; baseline table is generated; methodology is explicit.

7) **Plotting + reporting robustness**
- DoD: plots are produced deterministically; committed render assets are stable; no README rendering brittleness.

8) **Documentation coherence (“committee path”)**
- DoD: 30s/7m/15m path stays valid; docs cross-link correctly; no placeholders.

9) **Packaging + release hygiene**
- DoD: install extras are correct; versioning/release checklist is accurate; artifact evaluation instructions are consistent.

10) **Governance + policy completeness**
- DoD: SECURITY / citation / ethics / ownership notes are consistent and point to the right places.

## Top-20 (prioritized)

Each item has: goal, acceptance criteria, and likely files touched.

### 1) Add a “no Mermaid in README” guard
- Goal: prevent reintroducing brittle rendering blocks.
- Acceptance:
  - CI fails if `README.md` contains code fences tagged `mermaid`.
- Files:
  - `.github/workflows/ci.yml`
  - `scripts/` (new small grep script) OR inline bash in workflow
  - `README.md` (only if a note/link is added)

### 2) Add `make verify-results` (hash/manifest consistency)
- Goal: reviewers can check integrity without re-running full pipeline.
- Acceptance:
  - `make verify-results` validates `results/manifest.json` entries exist and match sha256 in repo.
  - Clear failure messages show which artifact mismatched.
- Files:
  - `Makefile`
  - `tools/verify_results.py` (new)

### 3) Define and validate a stable manifest schema
- Goal: avoid silent drift in `results/manifest.json` fields.
- Acceptance:
  - A JSON Schema exists and is checked in CI.
  - `make reproduce-all` produces schema-compliant manifest.
- Files:
  - `results/schema/manifest.schema.json` (new)
  - `tools/` (manifest writer / validator if needed)
  - `.github/workflows/ci.yml`

### 4) Ensure pipeline is “deterministic enough” under pinned deps
- Goal: reduce flaky diffs in plots / markdown tables.
- Acceptance:
  - Running `make reproduce-all` twice on same runner yields identical `results/manifest.json` and hashes.
  - If non-determinism remains, it is documented in `docs/LIMITATIONS.md`.
- Files:
  - `Makefile`
  - `tools/plot_results.py`
  - `docs/LIMITATIONS.md`

### 5) Add a single command “reviewer smoke check” target
- Goal: 7-minute path is one command.
- Acceptance:
  - `make reviewer-smoke` runs a minimal subset: quick tests + minimal pipeline artifacts.
  - Documented in README and/or docs.
- Files:
  - `Makefile`
  - `README.md` and/or `docs/ARTIFACT_EVALUATION.md`

### 6) Expand conformance corpus (10–20 new cases)
- Goal: broader coverage of semantics already claimed.
- Acceptance:
  - Add new programs and update corpus manifest.
  - CI runs conformance and produces a report artifact.
- Files:
  - `conformance/corpus/`
  - `conformance/manifest.json`
  - `tools/` (runner/report)
  - `.github/workflows/ci.yml`

### 7) Add minimized repro capture for conformance failures
- Goal: faster debugging and committee confidence.
- Acceptance:
  - When a conformance case fails, the report includes: program id, expected vs actual, diagnostic span/code.
- Files:
  - `tools/` (conformance runner)
  - `docs/DIAGNOSTICS_CONTRACT.md`

### 8) Differential testing (bounded) over VM-supported subset
- Goal: evidence that VM matches interpreter across many random programs.
- Acceptance:
  - A bounded generator exists with explicit unsupported-feature exclusions.
  - Seed is logged and failures are reproducible.
- Files:
  - `tests/` (property tests)
  - `tools/` (generator if not in tests)
  - `docs/CORRECTNESS.md` (method summary)

### 9) Tighten diagnostics contract tests (spans + codes)
- Goal: prevent drift between interpreter/VM diagnostics.
- Acceptance:
  - Add tests asserting spans/codes for a representative set.
- Files:
  - `tests/`
  - `docs/DIAGNOSTICS_CONTRACT.md`

### 10) Baseline methodology note (what baseline means)
- Goal: reviewers understand what’s being measured.
- Acceptance:
  - `results/baseline.md` remains generated; `results/README.md` explains methodology and environment sensitivity.
- Files:
  - `results/README.md`
  - `benchmarks/README.md`

### 11) Benchmark suite documentation parity
- Goal: each benchmark program has purpose + constraints.
- Acceptance:
  - Each benchmark folder documents inputs and expected behavior.
- Files:
  - `benchmarks/**/README.md`
  - `baseline_suite/README.md`

### 12) Plot output contract
- Goal: downstream docs rely on stable filenames.
- Acceptance:
  - Plot filenames are documented; pipeline always creates them.
- Files:
  - `tools/plot_results.py`
  - `docs/BENCHMARKS.md` and/or `results/README.md`

### 13) CI artifact bundle naming + index
- Goal: reviewers can download a single bundle and find everything.
- Acceptance:
  - CI uploads a single tar/zip with `results/` + key docs snapshot (optional).
  - Bundle contains `results/README.md` at top.
- Files:
  - `.github/workflows/ci.yml`
  - `scripts/bundle_artifacts.sh` (new)

### 14) Add “evidence map CI link-check”
- Goal: prevent broken internal links.
- Acceptance:
  - CI checks that linked files exist (at least within repo).
- Files:
  - `.github/workflows/ci.yml`
  - `scripts/check_links.py` (new, repo-local)

### 15) Roadmap → issue tracker mapping table
- Goal: make the plan auditable.
- Acceptance:
  - Add a section mapping issue IDs in this doc to GitHub issues once created.
- Files:
  - `docs/EXECUTION_PLAN.md`

### 16) Release checklist alignment with AE instructions
- Goal: reduce last-minute release drift.
- Acceptance:
  - Release checklist references the same commands as AE docs.
- Files:
  - `RELEASE_CHECKLIST.md`
  - `docs/ARTIFACT_EVALUATION.md` (or top-level)

### 17) Dependency pin policy note
- Goal: explain when pins are required vs flexible.
- Acceptance:
  - Document policy for dev vs CI vs AE; avoid pin explosion.
- Files:
  - `docs/REPRODUCIBILITY.md` (new or existing place)
  - `requirements*.txt` / `pyproject.toml` (as needed)

### 18) Security & disclosure triage template
- Goal: committee-ready governance.
- Acceptance:
  - Add a short template section in `SECURITY.md` about how issues are triaged.
- Files:
  - `SECURITY.md`

### 19) “No placeholders” lint for key docs
- Goal: avoid “...” placeholders reappearing in public-facing docs.
- Acceptance:
  - CI checks a small allowlist of files for `...` and fails if found.
- Files:
  - `.github/workflows/ci.yml`
  - `scripts/check_placeholders.sh` (new)

### 20) “15-minute path” drift test
- Goal: keep reviewer commands valid.
- Acceptance:
  - CI runs the documented 15-minute command path (or a close scripted equivalent).
- Files:
  - `.github/workflows/ci.yml`
  - `README.md` (only if command changes)

## Milestones (15–25 issues)

Milestones are intentionally small and acceptance-testable.
Issue IDs correspond to Top‑20 above.

### Milestone M0 — Guardrails (Week 1)
- Deliverable: CI prevents rendering/policy regressions; integrity checks exist.
- Issues: #1, #2, #3, #14, #19

### Milestone M1 — Evidence reliability (Weeks 2–3)
- Deliverable: results integrity + methodology clarity; stable plotting/report contract.
- Issues: #4, #10, #11, #12, #13, #20

### Milestone M2 — Conformance expansion (Weeks 4–6)
- Deliverable: more corpus coverage + better failure reporting + bounded differential testing.
- Issues: #6, #7, #8, #9

### Milestone M3 — Packaging & governance close-out (Weeks 7–8)
- Deliverable: release/AE alignment + dependency policy + security template.
- Issues: #15, #16, #17, #18

## Notes

- This plan deliberately avoids new language features (type system, macros, etc.).
- Where “CI check” is specified, prefer repo-local scripts under `scripts/` so checks are portable.
- Numeric results should remain artifact-driven under `results/` (no hard-coded numbers in docs).
