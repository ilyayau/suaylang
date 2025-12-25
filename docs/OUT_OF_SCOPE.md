# Out of scope

This document is an explicit boundary for what SuayLang does not claim to solve.
It is part of the falsifiability and committee-readiness contract.

## Not solved (by design)

- **Full semantic proof:** This artifact provides evidence-based equivalence over shipped corpora, not a mechanized proof for all programs.
- **Production language ecosystem:** No large standard library, package manager, or ecosystem-level guarantees.
- **Concurrency semantics:** No threads, async, or parallelism.
- **Macros / metaprogramming:** No macro system or compile-time evaluation.
- **Static typing research:** No type inference, no gradual typing claims.

## Known classes of false negatives (ways bugs could slip through)

- **Shared-oracle bugs:** If both backends share a flawed normalization or parser behavior, divergence may be masked.
- **Generator bias:** If fuzzing/generation exists, it may over-sample easy programs.
- **Unmodeled host effects:** Python runtime behaviors outside the language contract (e.g., environment-dependent timing) are not part of semantics.

## What bugs aren’t reliably caught

- Performance regressions not covered by reproduce-fast thresholds.
- Rare edge cases outside shipped corpora (unless explicitly added as regression tests).

## What evidence would expand scope (future work)

- Larger corpora + property-based generators with explicit coverage targets.
- Independent oracle checks (e.g., third implementation or cross-check against a separate semantics).

See also:
- docs/THREATS_TO_VALIDITY.md
- docs/LIMITATIONS.md
