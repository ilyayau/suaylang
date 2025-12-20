# Metrics (SuayLang)

This document defines the core metrics used in SuayLang’s research evaluation. All metrics are reported in `results/` artifacts and summarized in the README.

## 1. Diagnostic stability
- **Definition:** Percentage of error codes and primary span locations that remain unchanged across interpreter and VM for the same input corpus.
- **Formula:**
  - $\text{Stability} = \frac{\text{# matching (error code, span)}}{\text{# total errors}} \times 100$
- **Reported in:** `results/golden_diagnostics.md`, `results/diff_report.md`

## 2. Robustness (error kind classification)
- **Definition:** Percentage of programs for which the backend correctly classifies the error kind (lex, parse, runtime, internal) as compared to the reference.
- **Formula:**
  - $\text{Robustness} = \frac{\text{# correct error kind}}{\text{# total errors}} \times 100$
- **Reported in:** `results/diff_report.md`

## 3. Coverage
- **Definition:** Number of unique AST node kinds and opcode kinds observed in the test suite.
- **Breakdown:**
  - AST node kinds: e.g., Name, IntLit, Binary, Dispatch, etc.
  - Opcode kinds: e.g., LOAD, CONST, CALL, MATCH, etc.
- **Reported in:** `results/coverage.md`

## 4. Benchmarks (performance, not a claim)
- **Definition:** Median and p90 timings for parse, compile, interp, and VM phases, per benchmark program.
- **Reported in:** `results/benchmarks.md`

## 5. Baseline comparison
- **Definition:** Relative performance or correctness of a baseline (e.g., naive interpreter or raw-string diagnostics) vs. the current approach.
- **Reported in:** `results/baseline.md` (see TODO)

---

**All metrics are generated deterministically by `make research`.**

**TODO:**
- Add baseline.md with a concrete baseline table.
- If any metric is not yet implemented, add a TODO in the relevant runner script.
