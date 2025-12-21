# Known Intentional Imperfection

**Imperfection:**
The error messages for out-of-bounds errors in the baseline suite are minimal and do not provide full context (e.g., input values, call stack).

**Why it is kept:**
- Ensures the diagnostics contract is met with minimal implementation effort.
- Keeps the baseline implementation simple and auditable for equivalence testing.

**What it risks:**
- Reviewers may find the diagnostics less helpful for debugging.
- May obscure subtle differences in error reporting between implementations.

**How it is bounded:**
- All error cases are still detected and reported (no silent failures).
- The equivalence and observation policy are defined on error presence/type, not message detail.
- The technical report and diagnostics contract explicitly state this boundary.

**Correctness is not affected:**
- All correctness claims and equivalence tests are preserved.
