# ASCII syntax (legacy draft)

Canonical mapping table:

- [docs/ASCII_SYNTAX.md](../ASCII_SYNTAX.md)

The lexer accepts ASCII and Unicode spellings and normalizes them to canonical tokens.
Guarantee: the ASCII and Unicode programs parse to the same AST shape and evaluate identically (within the supported subset).

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
