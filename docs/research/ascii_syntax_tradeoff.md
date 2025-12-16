# ASCII syntax alternative (tradeoff note)

## Statement of intent

SuayLang is **Unicode-first**: the primary research syntax uses single-glyph operators and delimiters.

An ASCII alternative is provided as an **optional presentation layer** for:

- accessibility (keyboard layout constraints, screen readers, copy/paste environments), and
- communication in venues where Unicode input is difficult.

This document defines a **purely syntactic** mapping for core constructs. It does **not** change language semantics.

## Scope

The ASCII forms below are:

- intended for documentation, papers, and teaching materials,
- designed to be mechanically translatable to the Unicode surface syntax,
- **not claimed to be implemented** as a second parser in v0.1.

## Mapping table (Unicode → ASCII)

| Unicode | ASCII | Construct |
|---|---|---|
| `←` | `<-` | binding |
| `⇐` | `<~` | mutation |
| `▷` | `match` | dispatch head |
| `⇒` | `=>` | dispatch arm arrow |
| `⟲` | `cycle` | cycle head |
| `↩` | `continue` | cycle “continue” arm mode |
| `↯` | `finish` | cycle “finish” arm mode |
| `⟪` | `{` | block open |
| `⟫` | `}` | block close |

Notes:

- The intent is **unambiguous translation**, not minimal keystrokes.
- Mutation uses `<~` rather than `<=` to avoid clashing with the `≤`/`<=` comparison operator in ASCII-heavy settings.

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
