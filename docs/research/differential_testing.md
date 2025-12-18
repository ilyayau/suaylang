# Differential testing: Interpreter vs VM (v0.1 subset)

## Goal

Provide hard evidence for the hypothesis:

> The reference interpreter and the bytecode VM are observationally equivalent for the VM-supported subset.

Here, “observationally equivalent” is defined by the comparison policy in [suaylang/conformance.py](suaylang/conformance.py):

- **Termination**: `ok | lex | parse | runtime | internal`
- **Stdout**: exact match (normalized for CRLF vs LF)
- **Result value**: best-effort structural equality (if values are not comparable, the harness does not treat it as a divergence)
- **Errors**: coarse error class and source location (line/column) for diagnostics and runtime errors

This is intentionally conservative: it does **not** attempt to prove full semantic equivalence, only the subset exercised.

## Methodology

1. Generate $N$ randomized SuayLang programs from a **bounded, terminating** subset.
2. For each program:
   - Execute on the reference interpreter.
   - Compile and execute on the bytecode VM.
3. Compare the resulting observations using the shared policy.
4. If any mismatch occurs:
   - Save a reproducer (`program.suay`) and the two observations (`observations.json`).
   - Exit non-zero.

The runner is deterministic given a seed.

## Scope

**Included in fuzz generation (safe subset):**

- Literals: Int, Bool, Unit
- Aggregate literals: tuple `(a b)`, list `[a b c]`
- Variant values: `Ok•(payload)`, `Err•(payload)`
- Operators (binary): `+`, `−`, `×`, `%`, and comparisons `=`, `≠`, `<`, `≤`, `>`, `≥`
- Bindings (`←`)
- Calls (`·`) to a small builtin set: `say`, `text`, `map`, `fold`
- Dispatch and cycle appear via fixed templates (to exercise those constructs without generating non-terminating programs)

**Explicitly excluded:**

- Modules (`link`) and file IO
- Maps (`⟦ ⟧`) and map builtins (`keys/has/put`) in fuzz generation
- String literals beyond the `text` conversion path
- Unbounded loops / recursion
- Features not supported by the bytecode compiler

This is a testing subset, not a language redefinition.

## How to reproduce

From the repo root:

- Run differential fuzzing:
  - `python tools/conformance/fuzz_runner.py --n 5000 --seed 0`

On divergence, repro cases are written under:

- `tools/conformance/fuzz_failures/`

## Results

The following run was executed on 2025-12-16:

| Seed | N programs | Divergences | OK terminations | Runtime errors | Lex errors | Parse errors | Internal errors |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5000 | 0 | 3332 | 1668 | 0 | 0 | 0 |

### Bugs found and fixes applied

- **Divergences found (Interpreter vs VM):** 0
- **Engine bugs found during differential testing:** K = 0

Fixes applied during development were limited to the *testing harness* (generator constraints to keep the produced programs parseable and within the intended subset). No language semantics were changed.

Harness fixes applied (for reproducibility and valid-input generation):

- Avoid generating unary-minus numeric literals in positions that are syntactically ambiguous (emit `(0 − n)` instead of `-n`).
- Parenthesize variant payloads (`Tag•(payload)`) so nested variants parse unambiguously.
