# SuayLang v0.1 Language Contract

This document freezes what “SuayLang v0.1” means.

- The current Python implementation in `suaylang/` is the reference behavior for v0.1.
- This contract is written for engineering reviewers: it’s precise and intentionally non-promotional.

## 1) Scope and definitions

- **Program**: a sequence of expressions separated by newlines.
- **Expression**: every top-level form is an expression; evaluation produces a value.
- **Value**: runtime result (numbers, text, unit, bool, tuples/lists, maps, variants, closures, builtins).
- **Error**: user-facing “lexical error”, “syntax error”, or “runtime error” with spans; the CLI must not print Python tracebacks.

## 2) Supported language features (v0.1)

### 2.1 Lexing and tokens

- Unicode operators and delimiters as defined in `docs/GRAMMAR.md`.
- Newlines are significant (`NEWLINE` tokens separate top-level and block forms).
- Line comments: `⍝ ...` to end-of-line (newline is still tokenized).
- Strings: `"..."` with escapes `\n`, `\t`, `\"`, `\\`; raw newlines inside strings are rejected.
- Identifiers: Unicode letters + `_` start; continue with letters/digits/`_`.
- ASCII fallbacks are accepted for some operators (notably `*`/`/`/`-` for `×`/`÷`/`−`).

### 2.2 Core expressions and literals

Supported literal forms:

- `INT` and `DEC`
- `STRING`
- unit literal: `ø`
- booleans: `⊤` and `⊥`

Supported expression forms:

- Names: `ident`
- Binding: `name ← expr`
- Explicit mutation: `name ⇐ expr`
- Blocks: `⟪ ... ⟫` containing one or more expressions separated by newlines
- Grouping / tuples: `(expr)` for grouping; `(expr,)` for 1-tuple; multi-item tuples supported
- Lists: `[ ... ]`
- Maps: `⟦ key ↦ value , ... ⟧`
- Lambdas/closures: `⌁(pattern ...) expr` with lexical scoping
- Function application (curried): `f · x · y` (left-associative call chaining)
- Unary operators: `¬` and unary `−` (ASCII `-` accepted)
- Binary operators:
  - boolean: `∧`, `∨`
  - comparison: `=`, `≠`, `<`, `≤`, `>`, `≥`
  - arithmetic: `+`, `−`, `×`, `÷`, `%`
  - text/sequence concatenation: `⊞`

Operator precedence and associativity match `docs/GRAMMAR.md`.

### 2.3 Algebraic variants

- Variant construction: `Tag•payload` where `Tag` is an identifier.
- Variant values are pattern-matchable via `dispatch`/`cycle`.

### 2.4 Pattern matching: `dispatch`

- Form: `value ▷ ⟪ ▷ pat ⇒ expr ... ⟫`
- Arms are checked top-to-bottom; first match wins.
- Patterns supported:
  - wildcard `_`
  - name binding patterns (`x`)
  - literal patterns: `INT`, `DEC`, `STRING`, `ø`, `⊤`, `⊥`
  - tuple patterns and grouping (comma rule applies)
  - list patterns including rest: `[p1 p2 ⋯ rest]` where `rest` is an identifier or `_`
  - variant patterns: `Tag•pat`

### 2.5 Pattern-driven looping: `cycle`

- Form: `⟲ seed ▷ ⟪ ▷ pat ⇒ ↩ expr | ▷ pat ⇒ ↯ expr ... ⟫`
- Semantics:
  - Evaluate `seed` to an initial state.
  - Match state against arms top-to-bottom.
  - `↩ expr` evaluates to the next state and repeats.
  - `↯ expr` evaluates to the final result and terminates.
  - If no arm matches, runtime error.

### 2.6 Standard library (builtins)

The v0.1 builtins are the documented set in `docs/STDLIB.md`:

- IO: `say`, `hear`
- Text/sequence: `text`, `at`, `take`, `drop`
- Collections: `count`, `keys`, `has`, `put`
- Higher-order: `map`, `fold`
- Math: `abs`

Module loading exists as an MVP builtin:

- `link · path · name → value`

Notes:

- Builtins are curried by arity.
- Type mismatches raise user-facing runtime errors.

### 2.7 Implementation targets included in v0.1

- Interpreter semantics are part of v0.1.
- The bytecode compiler/VM exists and is supported as an implementation artifact, but its internal instruction set is not part of the *language* contract (see §4).

## 3) Explicitly NOT part of v0.1

The following are out of scope for v0.1 and may be added later, changed, or never added:

- Static typing, type annotations, type inference
- Exceptions as a language feature (`try/catch`, user-thrown exceptions)
- Modules as syntax (`import`/`export` keywords); only `link` exists
- Classes/objects, methods, prototypes, reflection
- Concurrency, async/await, channels
- Macros, compile-time evaluation, metaprogramming
- User-defined operators or custom precedence
- Pattern guards (`pat if cond`), exhaustiveness checking
- Destructuring bind syntax beyond patterns in `dispatch`/`cycle`/lambda params
- Tail-call guarantees
- Deterministic iteration ordering beyond what is described for maps/keys

## 4) Stability: what is stable vs. allowed to change

### 4.1 Stable in v0.1 (must not change incompatibly in 0.1.x)

- The surface syntax and grammar as described in `docs/GRAMMAR.md`:
  - tokens, operator meanings, precedence, associativity
  - newline significance rules (top-level and block separation)
  - meanings of `dispatch`, `cycle`, `λ` (closures), `←`, `⇐`, `·`
- Core runtime value semantics:
  - boolean operators are short-circuiting
  - pattern matching is first-match wins
  - mutation updates the nearest enclosing binding of that name (lexical scope)
- The existence and basic behavior of the v0.1 builtins listed in §2.6.
- Error *categories* (lex/syntax/runtime) and presence of span-based diagnostics.

### 4.2 Unstable / may change in v0.1.x

These may change without constituting a language-breaking change, as long as valid programs still run correctly:

- Exact wording of error messages and stack traces
- Pretty-printing formatting of values (e.g. spacing in list/map display)
- Performance characteristics (parser/VM optimizations)
- Bytecode format, instruction names, operand encoding, and disassembler output
- LSP and editor tooling behavior

### 4.3 Undefined or intentionally unspecified behavior

Code that relies on any of the following is not covered by compatibility guarantees:

- Exact ordering of map printing (except where the stdlib explicitly promises insertion order for `keys`)
- Exact numeric formatting/precision of `text · n`
- Relying on the exact shape of stack traces
- Using invalid indices where behavior is not documented (should raise runtime error, but message/details may vary)

## 5) Backwards-compatibility rules (v0.1)

For patch releases `0.1.x → 0.1.y`:

- **Source compatibility**: any program that is valid under the v0.1 grammar must remain valid.
- **Behavior compatibility**: evaluation results must be the same, except for:
  - unspecified formatting details (§4.2/§4.3)
  - error message wording (category and span must remain correct)
- **No new required syntax**: new features may be added, but existing syntax must continue to parse with the same meaning.

If a breaking change is unavoidable (e.g. to fix a security issue in the host environment), it must:

- be called out as a breaking change even if the version number is still `0.x`, and
- include a minimal migration note.

## 6) How future versions may evolve

### 6.1 v0.2+ may introduce breaking changes

Breaking changes are allowed in future minor versions (`0.2`, `0.3`, …), but must be handled responsibly:

- publish a migration guide
- provide mechanical rewrites when possible
- keep the language surface small (avoid feature creep)

### 6.2 Expected evolution areas (non-binding)

These are plausible directions, not commitments:

- module system formalization (syntax-level import/export) or compilation-aware modules
- richer pattern matching (guards, better diagnostics, exhaustiveness hints)
- additional tiny builtins if justified by expressive power
- VM improvements: better debug tables, call stacks, and parity with interpreter

## 7) Reference documents

- Grammar (reference for v0.1): `docs/GRAMMAR.md`
- Minimal builtins: `docs/STDLIB.md`
- Bytecode format (implementation detail): `docs/BYTECODE.md`
