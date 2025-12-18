# SuayLang Language Reference (Legacy draft)

This file is a historical draft. The canonical contract reference is:

- [docs/LANGUAGE_REFERENCE.md](../LANGUAGE_REFERENCE.md)

The canonical contract is maintained in `docs/LANGUAGE_REFERENCE.md`.

Tone and scope: this is a contract document, not marketing. When this reference conflicts with older docs, this reference wins for v0.1.

## Table of contents

1. [Lexical structure](#1-lexical-structure)
2. [Grammar](#2-grammar)
3. [Evaluation model](#3-evaluation-model)
4. [Values and runtime types](#4-values-and-runtime-types)
5. [Binding vs mutation](#5-binding-vs-mutation)
6. [Control flow as expressions](#6-control-flow-as-expressions)
7. [Scoping rules](#7-scoping-rules)
8. [Collections semantics](#8-collections-semantics)
9. [Strings & Unicode model](#9-strings--unicode-model)
10. [Numeric model](#10-numeric-model)
11. [Error model](#11-error-model)
12. [Modules](#12-modules)
13. [Interpreter↔VM equivalence requirements](#13-interpretervm-equivalence-requirements)
14. [Versioning & compatibility policy](#14-versioning--compatibility-policy)
15. [Undefined behavior / forbidden constructs](#15-undefined-behavior--forbidden-constructs)

---

## 1) Lexical structure

### 1.1 Source text and encoding

- Source files are UTF-8 text.
- Newlines separate *forms* at top-level and inside blocks.

### 1.2 Whitespace and comments

- Spaces and tabs are treated as whitespace.
- Newlines are significant separators in contexts where the grammar requires them.
- Line comments start with `#` and continue to end-of-line.

### 1.3 Identifiers

- Identifiers start with a Unicode letter or `_`.
- Identifier continuation characters are letters, digits, or `_`.
- `_` is reserved as a wildcard in patterns.

### 1.4 Unicode and ASCII syntax (normative)

The lexer **accepts both** Unicode operators and first-class ASCII aliases and normalizes them to canonical token lexemes.

- Canonicalization is implemented by the lexer’s canonical lexeme map.
- The reference mapping is in [docs/reference/ASCII_SYNTAX.md](ASCII_SYNTAX.md).

Normative guarantee: programs written in ASCII aliases and their Unicode equivalents must parse to the same AST shape.

---

## 2) Grammar

The grammar is as defined in [docs/GRAMMAR.md](../GRAMMAR.md), with the operator precedence table summarized in:

- [docs/reference/OPERATOR_TABLE.md](OPERATOR_TABLE.md)

---

## 3) Evaluation model

### 3.1 Strictness

- Evaluation is strict: function arguments are evaluated before application.

### 3.2 Order of evaluation (normative)

- Binary operators evaluate left operand first, then right.
- Function application `f · x` evaluates `f` then `x`.
- Tuples/lists/maps evaluate elements left-to-right.
- `dispatch` evaluates the scrutinee once; arms are tested top-to-bottom and only the selected arm expression is evaluated.
- `cycle` evaluates the seed once and then iterates; arms are tested top-to-bottom each iteration; only the selected arm expression is evaluated.

### 3.3 Short-circuit

- `∧` and `∨` are short-circuiting boolean operators.

---

## 4) Values and runtime types

Runtime values (dynamic):

- unit (`ø`)
- booleans (`⊤`, `⊥`)
- integers (Python `int` semantics)
- decimals (Python `float` semantics)
- text (Unicode strings)
- tuples, lists, maps
- variants `Tag•payload`
- closures
- builtins (curried)

Equality:

- Structural equality for primitive types and collections as defined by the interpreter (best-effort).
- Map keys must be hashable; unhashable keys raise a runtime error.

---

## 5) Binding vs mutation

- Binding: `name ← expr` defines a new name in the current environment.
- Mutation: `name ⇐ expr` updates an existing binding in the nearest enclosing environment containing that name.
  - If not found, runtime error.

---

## 6) Control flow as expressions

Normative semantics for core constructs is minimal and test-backed.

- `dispatch` semantics: see [docs/spec/control_flow.md](../spec/control_flow.md#dispatch-)
- `cycle` semantics: see [docs/spec/control_flow.md](../spec/control_flow.md#cycle-)

Return/break/continue:

- v0.1 has no `return`, `break`, `continue` statements. `cycle` uses explicit `↩`/`↯` arm modes.

---

## 7) Scoping rules

- Lexical scoping.
- Blocks introduce a new environment.
- `dispatch` and `cycle` arms evaluate in a fresh environment extended with pattern bindings.
- Lambdas capture their defining environment (closures).

Shadowing:

- Re-binding a name in the same scope is an error; binding in an inner scope shadows outer bindings.

---

## 8) Collections semantics

Lists:

- Lists are ordered sequences.

Maps:

- Maps use insertion-ordered semantics as implemented by Python dict.
- Determinism contract: in v0.1, map literal evaluation order and iteration order in builtins and text rendering are deterministic given the same program input.

Mutation during iteration:

- v0.1 does not specify concurrent mutation semantics beyond what is reachable through builtins; programs must not rely on mutating a map while iterating over it unless a future version defines it.

Sets:

- Sets are not a first-class literal in v0.1.

---

## 9) Strings & Unicode model

- Text values are Unicode strings.
- Indexing and slicing are not specified as primitives unless provided by builtins.
- Invalid UTF-8 sequences are rejected at file decode time by the host (Python) and are considered out-of-scope for language semantics.

---

## 10) Numeric model

Integers:

- Integers are unbounded (Python `int`). No overflow.

Decimals:

- Decimals follow IEEE-754 double semantics as implemented by Python `float`.

Division/modulo:

- `/` and `÷` perform numeric division using interpreter semantics.
- `%` matches Python remainder behavior for integers.

---

## 11) Error model

### 11.1 Error categories

- lex errors
- syntax errors
- runtime errors
- internal errors (reported as user-facing diagnostics where possible)

### 11.2 Determinism

- For the supported subset, evaluation and error classification is deterministic.

### 11.3 Error codes (contract-driven tooling)

SuayLang maintains a stable **error code catalog** intended for golden diagnostic tests and reviewer-auditable regressions.

- Catalog: [docs/reference/ERROR_CATALOG.md](ERROR_CATALOG.md)
- Default behavior: the interpreter/CLI prints human-readable diagnostics.
- Contract tooling mode: error codes may be included in formatted diagnostics when enabled by tooling.

---

## 12) Modules

v0.1 note:

- There is no `import` keyword.
- Modules are loaded by file path via the curried builtin `link`.
- The VM does not support modules in v0.1; module behavior is out-of-scope for interpreter↔VM equivalence.

---

## 13) Interpreter↔VM equivalence requirements

### 13.1 Observational equivalence (normative definition)

Two executions are observationally equivalent if they agree on:

- termination class: `ok` / `lex` / `parse` / `runtime` / `internal`
- stdout (normalized)
- value equality (best-effort structural equality)
- for errors: error class plus coarse (line, column) location

### 13.2 Supported subset

Equivalence is required only on the supported subset enumerated in:

- [docs/spec/supported_subset.md](../spec/supported_subset.md)

---

## 14) Versioning & compatibility policy

- v0.1.x may adjust non-semantic behavior (exact error wording, bytecode instruction names).
- v0.1.x must not change meaning of programs within the supported subset.
- Any breaking semantic change requires a v0.2 proposal (and should be feature-gated if introduced early).

---

## 15) Undefined behavior / forbidden constructs

This section lists behaviors that are either explicitly forbidden or treated as UB in v0.1.

- Relying on module loading in VM mode (out-of-scope; forbidden for equivalence claims).
- Depending on host-specific Unicode decoding errors.
- Relying on implementation-defined details not covered by the supported subset.
