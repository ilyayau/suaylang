# ASCII syntax (first-class, normative)

SuayLang accepts both Unicode spellings and ASCII spellings, and the lexer normalizes ASCII to canonical Unicode token lexemes.

Guarantee: an ASCII program and its Unicode-equivalent program must parse to the same AST shape.

## Operator and token mapping

| Unicode | ASCII | Meaning |
|---|---|---|
| `⟪` `⟫` | `{` `}` | block delimiters |
| `⟦` `⟧` | `[[` `]]` | map delimiters |
| `←` | `<-` | binding |
| `⇐` | `<~` | mutation |
| `↦` | `->` | map entry arrow |
| `⇒` | `=>` | arm arrow |
| `▷` | `|>` | dispatch |
| `⟲` | `~~` | cycle |
| `↩` | `>>` | cycle continue |
| `↯` | `<<` | cycle finish |
| `•` | `::` | variant constructor |
| `⋯` | `...` | list-rest pattern |
| `⌁` | `\` | lambda |
| `·` | `.` | application |
| `⊤` | `#t` | true |
| `⊥` | `#f` | false |
| `ø` | `#u` | unit |
| `¬` | `!` | not |
| `×` | `*` | multiply |
| `÷` | `/` | divide |
| `−` | `-` | minus |
| `⊞` | `++` | text concatenation |
| `≤` | `<=` | less-or-equal |
| `≥` | `>=` | greater-or-equal |
| `≠` | `!=` | not-equal |
| `∧` | `&&` | and |
| `∨` | `||` | or |

## Side-by-side example

Unicode:

```suay
inc ← ⌁(x) x + 1
v ← Ok•41
v ▷ ⟪
▷ Ok•n  ⇒ inc · n
▷ _     ⇒ 0
⟫
```

ASCII:

```suay
inc <- \(x) x + 1
v <- Ok::41
v |> {
|> Ok::n  => inc . n
|> _      => 0
}
```
