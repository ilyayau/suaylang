# SuayLang Grammar (Formal EBNF, matches current implementation)

This file is a formal grammar specification for the **current** SuayLang implementation.

It matches the behavior of:
- the lexer in [suaylang/lexer.py](../suaylang/lexer.py)
- the recursive-descent parser in [suaylang/parser.py](../suaylang/parser.py)

## Lexical conventions

- **Whitespace**: spaces, tabs, and `\r` are ignored.
- **Newlines** (`NEWLINE`) are significant.
- **Comments**: `⍝ ...` to end-of-line. (The newline itself is still tokenized.)
- **Strings**: `"..."` with escapes `\n`, `\t`, `\"`, `\\`. Strings cannot contain raw newlines.
- **Identifiers** (`IDENT`): Unicode letters plus `_` as start; continue with letters/digits/`_`.
- ASCII operator fallbacks exist: `*`/`/`/`-` are accepted for `×`/`÷`/`−`.

The lexer produces tokens for the glyph operators and delimiters used below.

## Precedence and associativity

From lowest precedence to highest (all binary operators are **left-associative**):

1. **Dispatch chaining**: `▷ ⟪ ... ⟫` (left-associative chaining)
2. `∨`
3. `∧`
4. Comparisons: `= ≠ < ≤ > ≥`
5. Additive: `+ − ⊞`
6. Multiplicative: `× ÷ %`
7. Prefix: `¬` and unary `−`
8. Call chaining: `·` (left-associative)
9. Primary forms (literals, names, blocks, lambdas, etc.)

Important implementation detail: **call binds tighter than prefix**.
So `¬ f · x` parses as `¬(f · x)`.

Additionally, the implementation allows prefix operators directly in **call arguments**,
so `f · -x` parses as `f · (−x)`.

## Grammar

Notation:
- Terminals are quoted (e.g. `"⟪"`).
- `A ::= ...` defines a rule.
- `[...]` is optional.
- `{...}` repeats zero or more times.

### Program structure

```
Program       ::= { NEWLINE } [ Expr { NEWLINE+ Expr } ] { NEWLINE } EOF
```

Top-level expressions **must** be separated by at least one newline.

### Expressions

```
Expr          ::= Dispatch

Dispatch      ::= OrExpr { "▷" "⟪" { DispatchArm } "⟫" }
DispatchArm   ::= "▷" Pattern "⇒" { NEWLINE } Expr { NEWLINE }

OrExpr        ::= AndExpr { "∨" AndExpr }
AndExpr       ::= CmpExpr { "∧" CmpExpr }
CmpExpr       ::= AddExpr { ("=" | "≠" | "<" | "≤" | ">" | "≥") AddExpr }
AddExpr       ::= MulExpr { ("+" | "−" | "⊞") MulExpr }
MulExpr       ::= Prefix { ("×" | "÷" | "%") Prefix }

Prefix        ::= ("¬" | "−" | "-") Call
              | Call

Call          ::= Variant { "·" Variant }

CallArg       ::= Variant
              | ("¬" | "−" | "-") Variant

Variant       ::= IDENT "•" Primary
              | Primary
```

### Primary forms

```
Primary       ::= Literal
              | Binding
              | Mutation
              | Name
              | TupleOrGroup
              | List
              | Map
              | Block
              | Lambda
              | Cycle

Binding       ::= IDENT "←" { NEWLINE } Expr
Mutation      ::= IDENT "⇐" { NEWLINE } Expr
Name          ::= IDENT
```

#### Tuple / grouping

Grouping vs tuple is determined by the presence of a comma:

- `(Expr)` is grouping (returns the inner expression)
- `(Expr,)` is a 1-tuple
- `(Expr Expr ...)` is a tuple (2+) where items can be separated by newlines or commas **or** by adjacency

Formal form:

```
TupleOrGroup  ::= "(" { NEWLINE }
                  [ Expr { TupleItemSep Expr } [ "," ] ]
                  { NEWLINE } ")"

TupleItemSep  ::= "," { NEWLINE }
               | NEWLINE+
```

Implementation note: in addition to `TupleItemSep`, the parser also accepts **adjacent** expressions as multiple tuple items because spaces are ignored by the lexer.

#### Lists

```
List          ::= "[" { NEWLINE }
                  [ Expr { ListItemSep Expr } ]
                  { NEWLINE } "]"

ListItemSep   ::= "," { NEWLINE }
               | NEWLINE+
```

Implementation note: like tuples, lists also accept **adjacent** expressions as separate items.
The glyph `⋯` is **not** allowed in list expressions (it is pattern-only).

#### Maps

```
Map           ::= "⟦" { NEWLINE }
                  [ MapEntry { MapSep MapEntry } ]
                  { NEWLINE } "⟧"

MapEntry      ::= Expr "↦" Expr
MapSep        ::= "," { NEWLINE }
               | NEWLINE+
```

Implementation note: map entries also accept adjacency between entries.

#### Blocks

Blocks are sequences of expressions **separated by newlines** (like the top level):

```
Block         ::= "⟪" { NEWLINE } BlockItem { NEWLINE+ BlockItem } { NEWLINE } "⟫"
BlockItem     ::= Expr
```

Empty blocks are rejected.

#### Lambdas

```
Lambda        ::= "⌁" "(" { NEWLINE }
                  [ Pattern { ParamSep Pattern } ]
                  { NEWLINE } ")" { NEWLINE } Expr

ParamSep      ::= "," { NEWLINE }
               | NEWLINE+
```

There is no distinct “function definition” form: a function definition is simply a **binding** whose value is a **lambda**.

#### Cycle (pattern-driven looping)

```
Cycle         ::= "⟲" { NEWLINE } CycleSeed "▷" "⟪" { NEWLINE } { CycleArm } "⟫"
CycleSeed     ::= OrExpr

CycleArm      ::= "▷" Pattern "⇒" ("↩" | "↯") { NEWLINE } Expr { NEWLINE }
```

The seed uses `OrExpr` (not full `Expr`) to avoid consuming the cycle’s required `▷`.

### Literals

```
Literal       ::= INT | DEC | STRING | "ø" | "⊤" | "⊥"
```

### Patterns

Patterns are used in `dispatch` arms and `cycle` arms.

```
Pattern       ::= VariantPattern | PatternAtom
VariantPattern::= IDENT "•" PatternAtom

PatternAtom   ::= "_"
              | Literal
              | IDENT
              | PatternTupleOrGroup
              | ListPattern

PatternTupleOrGroup
              ::= "(" { NEWLINE }
                  [ Pattern { PatItemSep Pattern } [ "," ] ]
                  { NEWLINE } ")"

PatItemSep    ::= "," { NEWLINE }
               | NEWLINE+

ListPattern   ::= "[" { NEWLINE }
                  [ Pattern { ListItemSep Pattern } ]
                  [ "⋯" (IDENT | "_") ]
                  { NEWLINE } "]"
```

As with tuple/grouping in expressions, pattern parentheses use the comma rule:
- `(p)` is grouping
- `(p,)` is a 1-tuple pattern

## Ambiguities and parser resolution

### 1) Grouping vs 1-tuple / n-tuple

Ambiguity: `(x)` could be either a group or a 1-tuple.

Parser rule (implemented):
- `(Expr)` is grouping
- `(Expr,)` is a 1-tuple

The same rule applies to pattern parentheses.

### 2) Cycle uses the same `▷` glyph as dispatch

Ambiguity: `⟲ seed ▷ ⟪ ... ⟫` could conflict with `seed ▷ ⟪ ... ⟫` (dispatch) because both use `▷`.

Parser resolution (implemented):
- The cycle seed is parsed as `OrExpr` (not full `Dispatch`), so the `▷` token after the seed is reserved for the cycle.

Effect: if you want a **dispatch expression** as the cycle seed, you must wrap it so it is parsed inside a primary grouping, e.g.:

```suay
⟲ (x ▷ ⟪ ▷ _ ⇒ 1 ⟫) ▷ ⟪ ▷ _ ⇒ ↯ 0 ⟫
```

Minimal fix option (if desired later, without redesign): require parentheses around dispatch seeds and update `CycleSeed ::= Expr` in the grammar + parser.

### 3) “Adjacency as separator” inside collections

Implementation behavior: inside `()`, `[]`, and `⟦⟧`, items can be separated by commas or newlines, but also by mere adjacency because spaces are ignored by the lexer.

This is convenient (`[1 2 3]`) but means the grammar is not purely delimiter-driven.
The parser resolves boundaries by parsing each element as a full `Expr` until a closing delimiter is reached.

## Modules (semantic note)

There is no `import` keyword. Modules are loaded by file path using the curried builtin `link` (interpreter feature):

- `m ← link · "./path/to/mod"`  (`.suay` extension is optional)
- `m · "name"` returns the value of the top-level binding `name` in that module.

Circular loads are rejected, and names starting with `_` are treated as private.
