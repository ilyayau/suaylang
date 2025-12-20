# Risks (and mitigations)

This is a reviewer-facing risk register: what could invalidate claims or reduce interpretability, and what we do about it.

## 1) VM subset gaps

**Risk:** the VM/compiler may lag the interpreter, shrinking the meaningful equivalence surface.

**Mitigation:** keep the claimed scope explicit ([docs/SPEC_V1_SCOPE.md](SPEC_V1_SCOPE.md)), and treat scope expansion as evidence-gated.

## 2) Observation-policy mismatch

**Risk:** the comparison policy is too strict (false alarms) or too loose (misses real drift).

**Mitigation:** document the policy precisely and keep it small; add stronger comparisons only when they are stable and backed by new goldens.

## 3) Diagnostics drift

**Risk:** even if semantics match, error spans/messages drift and reviewer-visible UX degrades.

**Mitigation:** golden diagnostics snapshots + stable error-code mapping; report counts under `results/`.

## 4) Module system ambiguity

**Risk:** module behavior is a major source of real-world complexity and can invalidate “usable tool” expectations.

**Mitigation:** keep module claims conservative; treat module-system spec work as a separate milestone and document what is currently exercised.

## 5) Unicode adoption / accessibility tension

**Risk:** Unicode syntax improves readability for some but harms accessibility and tooling portability.

**Mitigation:** ASCII-first contract is canonical; Unicode is an alias; tooling exposes syntax modes and reference sheets.

## 6) Benchmark noise / misinterpretation

**Risk:** microbenchmark results are noisy and can be misread as performance guarantees.

**Mitigation:** publish raw numbers + interpretability notes; frame benchmarks as trends, not claims.

## 7) Reproducibility erosion

**Risk:** results become unreproducible due to environment drift or scripts changing silently.

**Mitigation:** single entry-point runner (`make research`) that records environment metadata and regenerates the same `results/*` set.

## 8) Over-claiming

**Risk:** prose claims outpace what is actually measured.

**Mitigation:** every claim in README and docs links to a concrete artifact (`results/*.json`, `results/*.md`, `docs/*.md`, or tests).
