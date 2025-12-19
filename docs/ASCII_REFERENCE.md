# ASCII reference (canonical)

SuayLang’s canonical surface syntax is **ASCII**.
Unicode spellings are supported as aliases and must parse to the same AST.

If you prefer Unicode output formatting (REPL / `suay run` result printing), set:

- `SUAY_OUTPUT_SYNTAX=unicode`

See also: [docs/ASCII_SYNTAX.md](docs/ASCII_SYNTAX.md) for a narrative overview.

## Token mapping

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

Comments:

| ASCII (canonical) | Unicode (alias) |
|---|---|
| `// ...` | `⍝ ...` |

## Examples

### Hello world

```suay
say . "hello"
```

### Functions + application

```suay
square <- \(x) x * x
say . (square . 7)
```

### Collections (List / Map)

```suay
xs <- [1 2 3]

m <- [["a" -> 1, "b" -> 2]]

say . (text . xs)
say . (text . m)
```

### `dispatch` (pattern matching)

```suay
classify <- \(v)
  v |> {
  |> Ok::x  => x + 1
  |> Err::x => x + 2
  |> _      => 0
  }

say . (classify . (Ok::41))
```

### `cycle` (explicit state machine)

```suay
sum_to <- \(n)
  ~~ (Step::(1 0)) |> {
  |> Done::acc     => << acc
  |> Step::(i acc) => >> (
        (i > n) |> {
        |> #t => Done::acc
        |> #f => Step::(i + 1  acc + i)
        }
      )
  }

say . (sum_to . 10)
```
