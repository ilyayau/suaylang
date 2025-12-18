# SuayLang v1.0.0 — Scope Freeze (Phase 1)

Date: 2025-12-18

This document defines **exactly what is in v1.0.0** and what is out-of-scope.

Rules:
- Anything “IN v1” must have: **spec text + tests + stable error code**.
- If something is not ready, it must be **removed** or gated behind `E-FEATURE-NOT-IN-V1`.
- Unicode spellings remain supported as aliases, but **ASCII is canonical**.

---

## 1) v1 language features (IN)

### 1.1 Source and layout
- UTF-8 source text.
- Newlines are significant separators between top-level forms and block forms.
- Whitespace is insignificant except as token separators.
- Line comments:
  - canonical: `// ...` to end of line
  - alias: `⍝ ...`

### 1.2 Values
- Unit (`#u`, alias `ø`)
- Bool (`#t/#f`, aliases `⊤/⊥`)
- Int
- Dec
- Text
- Tuple
- List
- Map
- Variant values
- Closures

### 1.3 Expressions
- Names
- Binding and mutation
- Blocks (lexical scope)
- Grouping/tuples
- Lists and maps
- Variant construction
- Lambdas
- Function application (curried)
- Unary operators: logical-not, numeric negation
- Binary operators:
  - arithmetic: `+`, `-`, `*`, `/`, `%`
  - comparisons: `=`, `!=`, `<`, `<=`, `>`, `>=`
  - boolean: `&&`, `||` (short-circuit)
  - concatenation: `++`

### 1.4 Evaluation
- Strict evaluation everywhere.
- Deterministic **left-to-right** evaluation order for operands and arguments.
- `&&` and `||` are the only short-circuiting operators.

### 1.5 Pattern matching
- `dispatch` (first match wins)
- `cycle` (explicit continue/finish modes)
- Patterns:
  - wildcard `_`
  - binder names
  - literals (Int/Dec/Text/Bool/Unit)
  - tuples
  - lists with optional rest pattern
  - variants

### 1.6 Modules (v1 module system)
- Syntax-level `import` and `export`.
- Deterministic module name mapping from project sources:
  - filesystem `src/a/b.suay` maps to module name `a::b`.
- Explicit exports only (no implicit “everything exported”).
- Import cycle detection with stable error code and precise spans.
- Visibility:
  - unexported names are inaccessible from other modules.
  - `_private` names are never exportable.

### 1.7 Stdlib (v1 minimum)
Stdlib ships as modules (not intrinsic language features), with stable contracts + tests:
- `std/core`: print/assert/conversions
- `std/option_result`: Option/Result and combinators
- `std/collections`: List/Map/Set minimal operations
- `std/string`: split/trim/replace/starts_with/ends_with
- `std/fmt`: `format()`
- `std/path`, `std/fs`, `std/io`: minimal path + file IO

Host boundary:
- All IO/FS/path capabilities must go through an explicit host boundary module with versioning and stable errors.

---

## 2) ASCII-first policy (IN)

- Canonical spelling in documentation and formatter output is ASCII.
- Unicode spellings remain supported as aliases.
- Tooling may emit `W-UNICODE-SYNTAX` when Unicode spellings are used (configurable; non-fatal).

---

## 3) Diagnostics stability (IN)

- All user-facing failures must map to stable codes (`E-*` and optional `W-*`).
- Golden tests must exist for:
  - code-prefixed diagnostics
  - caret span rendering
- Interpreter and VM must agree on:
  - termination class
  - stdout
  - value
  - error code
  - primary span and caret rendering

---

## 4) Tooling contract (IN)

CLI commands required for v1:
- `suay doctor`
- `suay pkg init|build|add|lock`
- `suay run <file|module>`
- `suay check`
- `suay test` (runs project tests + conformance)
- `suay fmt` (ASCII default; `--unicode` supported)

Project files required for v1:
- `suay.toml` (name, version, entry, deps)
- `suay.lock` (minimal pinned deps)

---

## 5) Explicit out-of-scope (OUT)

The following are not part of the v1 contract:
- REPL stability (may be experimental or removed)
- LSP/VS Code extension stability
- bytecode format stability
- static typing
- macros/metaprogramming
- reflection/object system
- concurrency/async

Additionally OUT of v1:
- the current `link` builtin as the primary module interface (string-key member access)

---

## 6) What would break v1 compatibility

A change is v1-breaking if it changes any of:
- grammar/token meanings, precedence, or associativity
- newline significance rules
- evaluation order rules (left-to-right + short-circuit semantics)
- scoping and shadowing rules
- pattern matching semantics
- module resolution rules
- any stdlib API contract shipped in v1
- stable error code meanings or span policies

Allowed non-breaking changes (v1.x):
- performance improvements
- internal VM bytecode changes
- wording changes that do not change:
  - error code
  - span/caret position
  - stable message skeleton requirements
