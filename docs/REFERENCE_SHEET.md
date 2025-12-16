# SuayLang Reference Sheet (v0.1)

This is a short, scannable reference for writing SuayLang.

## 1) Syntax overview (cheat table)

| Concept | Syntax | Notes |
|---|---|---|
| Binding | `name ← expr` | Introduces a new binding in current scope |
| Mutation | `name ⇐ expr` | Updates an existing binding in an enclosing scope |
| Block | `⟪ ... ⟫` | Newlines separate expressions |
| Lambda | `⌁(pattern ...) expr` | Closures, lexical scope |
| Call (curried) | `f · x · y` | Left-associative application |
| Dispatch | `value ▷ ⟪ ▷ pat ⇒ expr ... ⟫` | First-match wins |
| Cycle | `⟲ seed ▷ ⟪ ▷ pat ⇒ ↩ expr | ▷ pat ⇒ ↯ expr ... ⟫` | Explicit state-machine loop |
| Variants | `Tag•payload` | Tagged value |
| Map | `⟦ key ↦ value, ... ⟧` | Keys must be hashable |

## 2) Values & literals

- Int: `123`
- Dec: `3.14`
- Text: `"hello"`
- Unit: `ø`
- Bool: `⊤` / `⊥`
- Tuple: `(1 2)` (grouping uses `(expr)`; 1-tuple uses `(expr,)`)
- List: `[1 2 3]`
- Map: `⟦ "a" ↦ 1, "b" ↦ 2 ⟧`
- Variant: `Ok•41`, `Err•"bad"`

## 3) Binding vs mutation (`←` vs `⇐`)

```suay
x ← 1
x ⇐ 2
```

- `←` fails if the name is already bound in the same scope.
- `⇐` fails if the name is not bound in any enclosing scope.

## 4) Blocks `⟪ ⟫`

```suay
x ← ⟪
  a ← 10
  b ← 20
  a + b
⟫
```

## 5) Functions (`⌁`), calling (`·`), currying

```suay
add ← ⌁(a b) a + b
say · (text · (add · 2 · 3))
```

Builtins are curried by arity; over-application is an error.

## 6) `dispatch` patterns (examples)

```suay
classify ← ⌁(v)
  v ▷ ⟪
  ▷ Ok•x  ⇒ "ok:" ⊞ (text · x)
  ▷ Err•m ⇒ "err:" ⊞ m
  ▷ _     ⇒ "unknown"
  ⟫

say · (classify · (Ok•41))
```

Common patterns:
- `_` wildcard
- `x` name binding
- literals (`1`, `"hi"`, `ø`, `⊤`, `⊥`)
- tuples/lists (including list rest: `[a b ⋯ rest]`)
- variants: `Tag•pat`

## 7) `cycle` (examples)

```suay
sum_to ← ⌁(n)
  ⟲ (Step•(1 0)) ▷ ⟪
  ▷ Done•acc     ⇒ ↯ acc
  ▷ Step•(i acc) ⇒ ↩ (
        (i > n) ▷ ⟪
        ▷ ⊤ ⇒ Done•acc
        ▷ ⊥ ⇒ Step•(i + 1  acc + i)
        ⟫
      )
  ⟫

say · (text · (sum_to · 5))
```

## 8) Errors / diagnostics

Errors are user-facing and include file/line/column when available:

```text
path/file.suay:1:14: runtime error: Undefined name 'z'
...source line...
             ^
```

The CLI must not print Python tracebacks.

## 9) Modules with `link` (MVP)

`link · path · name → value`

Example layout:
- `examples/modules/` contains `.suay` modules

Example use:

```suay
m ← link · "./examples/modules/math"
add ← m · "add"
say · (text · (add · 2 · 3))
```

## 10) CLI commands

- `suay doctor` — health check
- `suay run <file>` — run a program
- `suay run -e '<code>'` — run inline source (playground)
- `suay check <file>` — lex+parse only
- `suay ast <file>` — print AST
- `suay new <project-name>` — scaffold a starter project
- `suay repl` — interactive mode (experimental)
- `suay test` — run project tests (requires dev deps)
- `suay fmt` — placeholder (planned)
