# SuayLang Reference Sheet (ASCII alternative, v0.1)

This file is an accessibility aid.

- Unicode remains the primary, research-oriented surface syntax.
- The ASCII forms below are a **first-class alias layer**.
- Semantics are identical: ASCII and Unicode parse to the same AST (modulo spans).

See docs/syntax_mapping.md for the full mapping table.

## Core mapping table (Unicode → ASCII)

| Unicode | ASCII | Construct |
|---|---|---|
| `←` | `<-` | binding |
| `⇐` | `<~` | mutation |
| `▷` | `|>` | dispatch |
| `⇒` | `=>` | arm arrow |
| `⟲` | `~~` | cycle head |
| `↩` | `>>` | cycle arm mode: continue |
| `↯` | `<<` | cycle arm mode: finish |
| `⌁` | `\` | lambda |
| `•` | `::` | variant separator |
| `⟦⟧` | `[[ ]]` | map delimiters |
| `↦` | `->` | map entry arrow |
| `⟪` | `{` | block open |
| `⟫` | `}` | block close |

Notes:

- Call uses `.` as an ASCII alias for `·`.
- Booleans/Unit: `#t`/`#f`/`#u` are ASCII aliases for `⊤`/`⊥`/`ø`.

## Equivalent examples

### Example 1: binding + block

Unicode:

```suay
x ← ⟪
	a ← 10
	b ← 20
	a + b
⟫
```

ASCII (presentation):

```text
x <- {
	a <- 10
	b <- 20
	a + b
}
```

Semantics: identical.

### Example 2: dispatch

Unicode:

```suay
classify ← ⌁(v)
	v ▷ ⟪
	▷ Ok•x  ⇒ x + 1
	▷ Err•x ⇒ x + 2
	▷ _     ⇒ 0
	⟫
```

ASCII (presentation):

```text
classify <- \(v)
	v |> {
	|> Ok::x  => x + 1
	|> Err::x => x + 2
	|> _      => 0
	}
```

Semantics: identical.

### Example 3: cycle

Unicode:

```suay
⟲ (Step•(1 0)) ▷ ⟪
▷ Done•acc     ⇒ ↯ acc
▷ Step•(i acc) ⇒ ↩ Step•(i + 1  acc + i)
⟫
```

ASCII (presentation):

```text
~~ (Step::(1 0)) |> {
|> Done::acc     => << acc
|> Step::(i acc) => >> Step::(i + 1  acc + i)
}
```

Semantics: identical.
