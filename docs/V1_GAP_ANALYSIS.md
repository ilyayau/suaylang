# SuayLang v1.0.0 — Gap Analysis (Phase 0 Audit)

Date: 2025-12-18

This document is an engineering audit. It enumerates **what exists today (v0.1)** vs **what must be true for v1.0.0**.

It is intentionally strict:
- If a behavior is user-facing and not backed by **spec text + tests + stable error code**, it is a **gap**.
- If a feature cannot be implemented cleanly for v1, it must be **removed** or gated behind an explicit `E-FEATURE-NOT-IN-V1`.

---

## Executive summary

Current state is a strong **v0.1** core:
- Parser/lexer support ASCII aliases and Unicode spellings.
- Interpreter and bytecode VM are observationally equivalent for a subset (conformance corpus passes).
- Stable error code catalog exists, and there are a few golden snapshots.
- Formatter exists (`suay fmt`) and defaults to ASCII-first.

However, v1.0.0 requirements are substantially larger. The biggest blockers:

1) **Modules are not v1-ready**
- Today: an interpreter-only MVP builtin `link` loads files and reads members by string key.
- v1 requires: syntax-level `import`/`export`, deterministic resolver, cycle diagnostics with spans, and **VM parity**.
- v1 explicitly disallows string-key access as the primary module interface.

2) **Closed-loop tooling is incomplete**
- Today: `suay` has `run/check/ast/doctor/new/repl/fmt/test/ref/explain`.
- Missing: `suay pkg init|build|add|lock`, `suay run <module>`, `suay test` that runs project tests + conformance, and a project file contract (`suay.toml`, `suay.lock`).
- `suay new` currently generates **Unicode** syntax, violating ASCII-first canonical UX.

3) **Diagnostics stability is not yet v1-grade**
- Codes exist, but `error_code()` is derived from **message string matching** (brittle).
- Golden diagnostics count is very small (currently 3 code snapshots + 3 default snapshots).
- Conformance comparison does **not** compare: error codes, rendered caret output, or message skeleton.

4) **Stdlib is not a module-based, host-boundary stdlib**
- Today: only intrinsic builtins (`say`, `text`, `map`, …). No `std/*` modules.
- v1 requires: `std/core`, `std/option_result`, `std/collections`, `std/string`, `std/fmt`, `std/path`, `std/fs`, `std/io`.
- v1 requires explicit, documented host boundary; currently host behavior is spread across builtins.

5) **Contract/spec mismatches exist already** (must be resolved before v1 freeze)
- `docs/LANGUAGE_REFERENCE.md` currently states binding/mutation return unit, but interpreter/VM return the bound value.
- Parser error messages still mention Unicode spellings (e.g. “Expected ⟪ …”), which conflicts with “ASCII is canonical everywhere”.

---

## Current inventory (v0.1 snapshot)

### Language surface (implemented)
- Literals: Int, Dec, Text, Bool, Unit
- Collections: Tuple, List, Map
- Names, binding, mutation
- Blocks and lexical scoping
- Lambdas with pattern parameters; curried calling via call operator
- Operators: arithmetic, comparisons, boolean short-circuit, concat
- Pattern matching: `dispatch`
- Pattern-driven loop: `cycle` with explicit continue/finish

### ASCII-first status
- Lexer accepts extensive ASCII aliases and normalizes to canonical Unicode token lexemes.
- Formatter can rewrite sources to canonical ASCII (default) or canonical Unicode (`--unicode`).
- Docs and examples were recently moved to ASCII-first, but not yet enforced by CI.

### Diagnostics and contracts
- Error catalog exists: `docs/ERROR_CODES.md`.
- Contract-formatting exists via `suay --error-codes …` and `suay explain E-…`.
- Golden tests exist for:
  - default user-facing diagnostics (small set)
  - error-code prefixed diagnostics (small set)

### Tooling
- CLI commands exist: `run`, `check`, `ast`, `doctor`, `new`, `repl`, `fmt`, `test`, `ref`, `explain`.
- CI runs `pytest` and conformance runner.

### Modules (current)
- Interpreter-only builtin `link`:
  - Loads a module file (relative to the importing file).
  - Exposes values by string member lookup.
  - Rejects private `_name`.
  - Detects cycles; caches modules per run.
- VM: no module support.

### Stdlib (current)
- Intrinsic builtins (not modules): IO (`say`, `hear`), conversions (`text`), collections operations (`keys`, `put`, …), higher-order (`map`, `fold`), math (`abs`).

---

## v1.0.0 requirements vs current state

Legend: ✅ done / 🟡 partial / ❌ missing

1) Stable language contract (single canonical spec matches behavior)
- 🟡 `docs/LANGUAGE_REFERENCE.md` exists, but has at least one mismatch (binding/mutation return value vs unit).
- 🟡 Several semantics are still only implied by implementation.

2) Closed-loop UX (install/init/run/test/fmt under 60s)
- 🟡 Install works via editable install; no one-command user path (pipx/wheel) is documented as primary.
- ❌ Project init via `suay pkg init` missing.
- 🟡 `suay new` exists but is not a v1 project contract and emits Unicode.

3) ASCII-first canonical everywhere
- 🟡 Formatter is ASCII-first; lexer supports ASCII.
- 🟡 Docs/examples mostly ASCII-first.
- ❌ Parser/diagnostic messages still use Unicode glyphs in wording.
- ❌ No `W-UNICODE-SYNTAX` warning pipeline.

4) Real modules
- ❌ No syntax-level modules.
- ❌ No deterministic resolver spec.
- ❌ No VM parity.
- ✅ Cycle detection exists in interpreter (for `link`), but wrong interface for v1.

5) Interpreter ↔ VM observational equivalence for entire v1 feature set
- 🟡 Conformance exists for current subset.
- ❌ Not covering modules, module-based stdlib, or host boundary.
- ❌ Comparer does not compare error code + caret rendering.

6) Diagnostics stable (versioned error codes, golden-tested)
- 🟡 Error codes exist; some golden snapshots exist.
- ❌ Code assignment currently depends on message string matching.
- ❌ Target counts (>=120 golden diagnostics) not met.

7) Minimal stdlib exists, documented, tested
- 🟡 Builtins exist and are documented.
- ❌ Required `std/*` modules don’t exist.
- ❌ Host boundary is not explicit.

8) CI is green and enforces all of the above
- 🟡 CI green for tests + current conformance.
- ❌ CI does not enforce ASCII-first via `suay fmt --check`.
- ❌ CI does not enforce `suay test` as the single contract runner.

9) Releases are real
- ❌ Version is 0.1.0.
- 🟡 CHANGELOG exists (0.1.0 entry).
- ❌ v1 release checklist and migration content not present.

---

## Underspecified or inconsistent semantics (must resolve before v1 freeze)

### A) Binding/mutation return value
- Spec currently says: binding/mutation return unit.
- Implementation returns: the RHS value (both interpreter and VM).

Decision required:
- Either (1) change the implementation to return unit, or (2) update the spec to say binding/mutation return the RHS value.
- This affects many programs and should be frozen early.

### B) Canonical spelling in diagnostics
- ASCII-first requires user-visible docs and tooling be ASCII canonical.
- Parser errors currently talk about Unicode tokens (e.g. “Expected ⟪ …”, “Expected ⟫ …”).

Decision required:
- v1 diagnostics must reference ASCII spellings in messages.
- Unicode glyphs may still be accepted in source, but message wording must not force Unicode literacy.

### C) Text formatting of values
- `_to_text()` prints values using Unicode formatting (e.g. `⟦` / `↦`).

Decision required:
- v1 must decide whether runtime text representation is:
  - ASCII canonical (preferred for adoption), or
  - Unicode canonical (allowed but conflicts with “ASCII-first everywhere” unless explicitly scoped).

### D) Error-code stability mechanism
- Today `error_code(e)` derives code by matching message strings.

Decision required:
- v1 must attach codes at the source of the error (lexer/parser/runtime/builtins) or via a structured error type.

---

## VM ↔ interpreter mismatches / parity gaps

### Hard mismatch
- Modules: interpreter supports `link`, VM does not.

### Parity gaps in evidence
- Conformance only compares:
  - termination class
  - stdout
  - value
  - error type and primary span location
- v1 requires comparing:
  - error **code**
  - stable **message skeleton**
  - stable **caret rendering**

### Risky area
- Short-circuit and evaluation order depend on operator lexeme (Unicode vs ASCII).
- Compiler currently special-cases Unicode `∧`/`∨`, not ASCII `&&`/`||`.
  - This is a correctness risk once the formatter and docs go ASCII-first.

---

## Tooling gaps (closed-loop UX)

### Missing commands
- `suay pkg init|build|add|lock` (required)
- `suay run <module>` (required)

### Existing command issues
- `suay new` generates Unicode syntax and isn’t a v1 project contract (needs replacement or re-scope).
- `suay doctor` embeds Unicode syntax in its internal check program.
- `suay test` runs `pytest` only; does not run conformance/stdlib contract tests.

### Project file contract missing
- `suay.toml` and `suay.lock` do not exist.

---

## Module system gaps (v1)

Current: `link` builtin + string member access.

Required for v1:
- Syntax-level imports/exports:
  - `import a::b` (or similar)
  - `export { name1 name2 }` (or equivalent)
- Deterministic resolution algorithm:
  - mapping from filesystem paths (`src/a/b.suay`) to module names (`a::b`)
  - project root selection and search paths
  - stable error codes for not-found, parse error in dependency, access to non-exported, etc.
- Cycle detection with clear cycle chain and precise spans
- Visibility rules (public/private)
- VM parity: module compilation/execution model must match interpreter

Additionally for v1:
- No string-key member access as the primary module interface.
  - This means: `link` is either removed from v1, or moved to a host-boundary module and explicitly OUT-of-contract.

---

## Stdlib gaps (v1)

Current state: intrinsic builtins only.

Required for v1:
- Module-based stdlib with contracts + tests:
  - `std/core`
  - `std/option_result`
  - `std/collections`
  - `std/string`
  - `std/fmt`
  - `std/path`, `std/fs`, `std/io`

Host boundary requirement:
- Any IO/FS must pass through an explicit host boundary module with stable errors.
- Current builtins `say/hear` are direct host calls and are not behind a boundary.

---

## Diagnostics gaps (v1)

- Error code assignment is brittle (string matching).
- Golden diagnostics are far below target (currently 3 code snapshots).
- No warnings pipeline (needed for `W-UNICODE-SYNTAX`).
- Conformance does not compare error-code/caret rendering.

---

## CI + enforcement gaps (v1)

Current CI:
- runs `pytest`
- runs conformance corpus

Missing enforcement:
- `suay fmt --check` on docs/examples (ASCII-first regression guard)
- `suay test` as canonical runner (tests + conformance + future stdlib tests)
- nightly/optional differential runner (seeded, large N)

---

## Clear cut list: IN v1 vs OUT of v1

### IN v1 (must ship with spec + tests + stable errors)
- Core language semantics already present:
  - values, literals, collections
  - strict evaluation order (left-to-right)
  - blocks, scoping, shadowing rules
  - bind vs mutate semantics
  - lambdas, call semantics
  - `dispatch` and `cycle`
  - pattern language
- ASCII-first canonical surface:
  - docs/examples ASCII
  - formatter ASCII default
  - Unicode aliases accepted
  - optional warning `W-UNICODE-SYNTAX`
- Module system v1:
  - `import`/`export`
  - deterministic resolution
  - cycle detection with `E-IMPORT-CYCLE`
  - VM parity
- Stdlib v1 minimum as modules with contracts + tests:
  - `std/core`, `std/option_result`, `std/collections`, `std/string`, `std/fmt`
  - `std/path`, `std/fs`, `std/io` via explicit host boundary
- Tooling v1:
  - `suay pkg init|build|add|lock`
  - `suay run <file|module>`
  - `suay check`, `suay test`, `suay fmt`, `suay doctor`
- Diagnostics stability:
  - versioned error codes
  - golden diagnostics
  - conformance comparing code + caret
- CI enforcement for all the above

### OUT of v1 (explicitly not promised)
- Current `link` builtin (string-key access) as a primary module interface
- REPL contract stability (can remain experimental or be removed)
- LSP/VS Code extension contract
- Bytecode format stability
- Static typing / inference
- Macros/metaprogramming
- Reflection/object system

---

## Risk-ranked cutlist (what to do first)

P0 blockers (must be solved early):
1) Decide and freeze binding/mutation return value.
2) Fix compiler short-circuit to support ASCII `&&`/`||` (and keep Unicode aliases).
3) Replace message-based error code mapping with structured codes.
4) Design and implement module system v1 with VM parity.

P1 (needed for “reviewer-friendly v1”):
- Expand golden diagnostics to cover all stable errors and typical failures.
- Expand conformance runner to compare error code + caret output.
- Implement `suay pkg` and project file contract.

P2 (scale evidence):
- Hit target counts for conformance and golden diagnostics.
- Add seeded generator / nightly fuzz with published report.

---

## Notes / evidence pointers

This audit is based on the current repository state:
- CLI surface: `suaylang/cli.py`
- Lexer/parser: `suaylang/lexer.py`, `suaylang/parser.py`
- Interpreter + module MVP: `suaylang/interpreter.py`
- VM/compiler: `suaylang/vm.py`, `suaylang/compiler.py`
- Error catalog + code mapping: `docs/ERROR_CODES.md`, `suaylang/contract.py`
- Golden diagnostics tests: `tests/test_golden_diagnostics.py`, `tests/test_golden_error_codes.py`
- Conformance: `suaylang/conformance.py`, `tools/conformance/run.py`, `conformance/corpus/`
