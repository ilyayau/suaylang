# SuayLang Reference Sheet (ASCII alternative, v0.1)

This file is an accessibility aid.

- Unicode remains the primary, research-oriented surface syntax.
- The ASCII forms below are an **optional presentation layer** for documentation and teaching.
- Semantics are identical: each ASCII form is intended to be mechanically translatable to the Unicode form.

This document does not claim that an ASCII parser is implemented in v0.1.

## Core mapping table (Unicode → ASCII)

| Unicode | ASCII | Construct |
|---|---|---|
| `←` | `<-` | binding |
| `⇐` | `<~` | mutation |
| `▷` | `match` | dispatch head |
| `⇒` | `=>` | dispatch arm arrow |
| `⟲` | `cycle` | cycle head |
| `↩` | `continue` | cycle arm mode: continue |
| `↯` | `finish` | cycle arm mode: finish |
| `⟪` | `{` | block open |
| `⟫` | `}` | block close |

Notes:

- Mutation uses `<~` (not `<=`) to avoid clashing with comparison operators in ASCII-heavy settings.
- This table focuses only on the constructs required for the optional ASCII layer.

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
classify <- fn(v)
	match v {
	match Ok•x  => x + 1
	match Err•x => x + 2
	match _     => 0
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
cycle (Step•(1 0)) match {
match Done•acc     => finish acc
match Step•(i acc) => continue Step•(i + 1  acc + i)
}
```

Semantics: identical.
