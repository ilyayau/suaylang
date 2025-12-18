# ASCII syntax (canonical) + Unicode aliases

SuayLang supports two surface spellings:

- **ASCII is canonical** (docs/examples/formatter default).
- Unicode spellings remain supported as **aliases**.

Guarantee: an ASCII program and its Unicode-equivalent program must parse to the same AST shape.

## Operator and token mapping

| ASCII (canonical) | Unicode (alias) | Meaning |
|---|---|---|
| `{` `}` | `⟪` `⟫` | block delimiters |
| `[[` `]]` | `⟦` `⟧` | map delimiters |
| `<-` | `←` | binding |
| `<~` | `⇐` | mutation |
| `->` | `↦` | map entry arrow |
| `=>` | `⇒` | arm arrow |
| `|>` | `▷` | dispatch |
| `~~` | `⟲` | cycle |
| `>>` | `↩` | cycle continue |
| `<<` | `↯` | cycle finish |
| `::` | `•` | variant constructor |
| `...` | `⋯` | list-rest pattern |
| `\` | `⌁` | lambda |
| `.` | `·` | application |
| `#t` | `⊤` | true |
| `#f` | `⊥` | false |
| `#u` | `ø` | unit |
| `!` | `¬` | not |
| `*` | `×` | multiply |
| `/` | `÷` | divide |
| `-` | `−` | minus |
| `++` | `⊞` | concatenation (Text/List/Map) |
| `<=` | `≤` | less-or-equal |
| `>=` | `≥` | greater-or-equal |
| `!=` | `≠` | not-equal |
| `&&` | `∧` | and |
| `||` | `∨` | or |

ASCII-only comment syntax:

| ASCII (canonical) | Unicode (alias) | Meaning |
|---|---|---|
| `// ...` | `⍝ ...` | line comment |

## Side-by-side example

ASCII (canonical):

```suay
inc <- \(x) x + 1
v <- Ok::41
v |> {
|> Ok::n  => inc . n
|> _      => 0
}
```

Unicode (alias):

```suay
inc ← ⌁(x) x + 1
v ← Ok•41
v ▷ ⟪
▷ Ok•n  ⇒ inc · n
▷ _     ⇒ 0
⟫
```
