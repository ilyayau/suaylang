# SuayLang Language Reference (Canonical Contract, v0.1)

This document is the single source-of-truth specification for SuayLang v0.1.

- When this reference conflicts with older docs, **this reference wins**.
- The **reference interpreter** defines normative behavior; the bytecode VM must be observationally equivalent on the supported subset.

See also:
- [docs/ASCII_SYNTAX.md](ASCII_SYNTAX.md) — first-class ASCII spellings (normative)
- [docs/ERROR_CODES.md](ERROR_CODES.md) — stable diagnostic codes (normative)

## 1. Source text

- Source files are UTF-8 text. If a file cannot be decoded as UTF-8, the CLI must fail with `E-UTF8`.
- Whitespace is insignificant **except** where it separates tokens.
- Newlines are separators between top-level forms and between forms inside blocks.

## 2. Evaluation model (strict)

### 2.1 Strict evaluation

Evaluation is eager everywhere.

### 2.2 Order of evaluation (left-to-right)

Decision #1 (contract): evaluation order is **strict left-to-right**.

- Binary operators evaluate the left operand first, then the right operand.
- Function application `f · x` evaluates `f` then `x`.
- Tuple/list/map literals evaluate elements left-to-right.

Notes:

- Short-circuit operators (`∧`, `∨`) are a deliberate exception: they may skip RHS evaluation.

### 2.3 Control-flow evaluation

- `dispatch` evaluates the scrutinee exactly once; arms are tested top-to-bottom; only the selected arm expression is evaluated.
- `cycle` evaluates the seed exactly once; on each iteration arms are tested top-to-bottom; only the selected arm expression is evaluated.

### 2.4 Boolean short-circuit

- `∧` and `∨` are short-circuiting operators.

## 3. Values

### 3.1 Unit

- Unit is the unique empty value.
- The canonical surface spelling is `ø`.

### 3.2 Booleans

- True: `⊤` (ASCII `#t`)
- False: `⊥` (ASCII `#f`)

### 3.3 Numbers

- `Int` literals are parsed into Python integers in v0.1.
- `Dec` literals are IEEE-754 doubles (Python `float`) in v0.1.

### 3.4 Text

- Text is Unicode string data.

## 4. Binding and mutation

- Binding: `name ← expr` defines a new name in the current scope.
- Mutation: `name ⇐ expr` updates an existing binding in the nearest enclosing scope.
- Both binding and mutation evaluate their RHS and return unit.

## 5. Blocks and scoping

- Blocks `⟪ ... ⟫` introduce a new scope.
- Inside a block, each form must end at a newline or block end.

## 6. Equality

- Equality is structural for primitive values and collections.
- Map keys must be hashable.

## 7. Error model (contract)

- Errors are deterministic and include a stable code plus a source location (line/column).
- Default diagnostics are human-readable.
- Contract-mode tooling may include codes (e.g., golden diagnostics).

Codes are defined in [docs/ERROR_CODES.md](ERROR_CODES.md).

## 8. Interpreter ↔ VM equivalence

For conformance, interpreter and VM executions must be observationally equivalent (within the supported subset) by comparing:

- termination class (ok/runtime/lex/syntax)
- stdout
- returned value (when ok)
- error type and primary span location

## Appendix A. Legacy references

Historical drafts live under `docs/reference/`. They are not canonical for v0.1.
