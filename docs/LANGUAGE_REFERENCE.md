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

### 1.1 Canonical surface spelling (ASCII-first)

The canonical spelling for v0.1 docs and tooling is **ASCII** (see [docs/ASCII_SYNTAX.md](ASCII_SYNTAX.md)).

Unicode spellings are supported as aliases and must be equivalent.

## 2. Evaluation model (strict)

### 2.1 Strict evaluation

Evaluation is eager everywhere.

### 2.2 Order of evaluation (left-to-right)

Decision #1 (contract): evaluation order is **strict left-to-right**.

- Binary operators evaluate the left operand first, then the right operand.
- Function application `f . x` evaluates `f` then `x`.
- Tuple/list/map literals evaluate elements left-to-right.

Notes:

- Short-circuit operators (`&&`, `||`) are a deliberate exception: they may skip RHS evaluation.

### 2.3 Control-flow evaluation

- `dispatch` evaluates the scrutinee exactly once; arms are tested top-to-bottom; only the selected arm expression is evaluated.
- `cycle` evaluates the seed exactly once; on each iteration arms are tested top-to-bottom; only the selected arm expression is evaluated.

### 2.4 Boolean short-circuit

- `&&` and `||` are short-circuiting operators.

## 3. Values

### 3.1 Unit

- Unit is the unique empty value.
- Canonical ASCII spelling: `#u`.
- Unicode alias: `ø`.

### 3.2 Booleans

- True: `#t` (Unicode alias `⊤`)
- False: `#f` (Unicode alias `⊥`)

### 3.3 Numbers

- `Int` literals are parsed into Python integers in v0.1.
- `Dec` literals are IEEE-754 doubles (Python `float`) in v0.1.

### 3.4 Text

- Text is Unicode string data.

### 3.5 Tuples, lists, and maps

- Tuple values are ordered fixed-size sequences.
- List values are ordered sequences.
- Map values are key/value dictionaries.
	- Map keys must be hashable.
	- Map literals evaluate entries left-to-right.

### 3.6 Variants

- Variant values are tagged values: `Tag::payload` (Unicode alias `Tag•payload`).
- `Tag` is an identifier.

### 3.7 Closures and builtins

- A lambda evaluates to a closure that captures its lexical environment.
- Builtins are always available names provided by the runtime.

## 4. Truthiness

Truthiness is used by short-circuit operators and control constructs implemented via those operators.

- `#f` is false.
- `#u` is false.
- All other values are truthy.

## 5. Binding, mutation, and shadowing

### 5.1 Binding (`<-`)

- `name <- expr` evaluates `expr` in the current environment.
- If `name` is already bound in the *current* scope, it is a runtime error (`E-NAME`).
- Otherwise it introduces a new binding for `name` in the current scope.
- The expression evaluates to the RHS value.

### 5.2 Mutation (`<~`)

- `name <~ expr` evaluates `expr` in the current environment.
- It updates the nearest enclosing scope that already contains `name`.
- If `name` is not bound in any enclosing scope, it is a runtime error (`E-NAME`).
- The expression evaluates to the RHS value.

### 5.3 Shadowing

- A nested scope may bind the same name as an outer scope (shadowing).
- Shadowing affects name lookup lexically: the innermost binding is used.

## 6. Blocks and scoping

- Blocks `{ ... }` introduce a new lexical scope.
- Inside a block, forms are separated by newlines.
- A block must contain at least one expression; empty blocks are a syntax error.
- The value of a block is the value of its last expression.

At the top level:
- A program is a sequence of expressions separated by newlines.
- The value of a program is the value of its last expression (or `#u` if there are no expressions).

## 7. Function values and application

### 7.1 Lambda

- Lambda syntax: `\(p1 p2 ...) body`.
- Parameters are patterns.
- Lambdas are closures with lexical scoping.

### 7.2 Application (`.`)

- Application syntax is left-associative: `f . x . y` means `(f . x) . y`.
- Application evaluates `f` first, then `x`.

Calling a closure:
- If the argument does not match the first parameter pattern, it is a runtime error.
- If there are remaining parameters, the result is a new closure with remaining parameters.
- If all parameters are satisfied, the result is the evaluated body.

Calling a builtin:
- Builtins are curried by arity.
- Over-application is a runtime error.

## 8. Operators

### 8.1 Unary operators

- `! x` (Unicode alias `¬ x`) returns the boolean negation of the truthiness of `x`.
- `- x` (Unicode alias `− x`) is numeric negation and requires a number.

### 8.2 Binary operators

- Arithmetic operators require numbers.
- Comparison operators require either numbers or text (as defined per operator).
- `++` concatenates text and sequence-like values where defined.

### 8.3 Short-circuit boolean operators

- `&&` and `||` are short-circuiting.
- `a && b` evaluates `a`; if `a` is falsy, it returns `#f` without evaluating `b`. Otherwise it evaluates `b` and returns its truthiness as a boolean.
- `a || b` evaluates `a`; if `a` is truthy, it returns `#t` without evaluating `b`. Otherwise it evaluates `b` and returns its truthiness as a boolean.

## 9. Pattern matching: `dispatch`

Syntax (ASCII canonical):

```suay
value |> {
|> pat1 => expr1
|> pat2 => expr2
}
```

Semantics:
- The scrutinee `value` is evaluated exactly once.
- Arms are tested top-to-bottom.
- The first matching arm is selected.
- Only the selected arm expression is evaluated.
- Arm-bound names are scoped to the selected arm.
- If no arm matches, it is a runtime error (`E-NOMATCH`).

## 10. Pattern-driven looping: `cycle`

Syntax (ASCII canonical):

```suay
~~ seed |> {
|> pat1 => >> next_state_expr
|> pat2 => << result_expr
}
```

Semantics:
- The seed is evaluated exactly once to produce the initial state.
- Each iteration matches the current state against arms top-to-bottom.
- `>> expr` evaluates `expr` to produce the next state and repeats.
- `<< expr` evaluates `expr` to produce the final result and terminates.
- If no arm matches, it is a runtime error (`E-NOMATCH`).

## 11. Modules (v0.1)

v0.1 does not have syntax-level `import`/`export`.

The only supported module mechanism is the builtin `link` (interpreter feature):

- `m <- link . "./path/to/mod" . "name"` returns a value from a loaded module.

Module-loading rules (current contract for v0.1):
- Paths are resolved relative to the importing file.
- Loads are cached within a single run.
- Import cycles are rejected.
- Names beginning with `_` are private and cannot be accessed.

Note: module loading is not implemented by the bytecode VM in v0.1 and is outside interpreter↔VM conformance.

## 12. Standard library (v0.1)

The v0.1 standard library is a set of always-available builtins. Contracts are documented in [docs/STDLIB_REFERENCE.md](STDLIB_REFERENCE.md).

## 13. Error model (contract)

- Errors are deterministic and include a stable code plus a source location (line/column).
- Errors are categorized as lexical, syntax, or runtime.
- Default diagnostics are human-readable.
- Contract-mode tooling may include stable codes.

Codes are defined in [docs/ERROR_CODES.md](ERROR_CODES.md).

## 14. Interpreter ↔ VM equivalence

For conformance, interpreter and VM executions must be observationally equivalent (within the supported subset) by comparing:

- termination class (ok/runtime/lex/syntax)
- stdout
- returned value (when ok)
- error type and primary span location

## Appendix A. Legacy references

Historical drafts live under `docs/reference/`. They are not canonical for v0.1.
