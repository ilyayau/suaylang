# SuayLang Unicode ↔ ASCII syntax mapping (v0.1)

SuayLang is **Unicode-first**: the official surface syntax uses single-glyph operators and delimiters.

To reduce the entry barrier (keyboard layouts, accessibility, copy/paste constraints), SuayLang also supports a **first-class ASCII alias layer**. ASCII and Unicode programs parse to the **same AST** (modulo source spans), and evaluate with identical semantics.

## Core token mapping

| Unicode token | ASCII alias(es) | Notes |
|---|---|---|
| `←` | `<-` | binding |
| `⇐` | `<~` | mutation (explicit assignment) |
| `⟪` | `{` | block open |
| `⟫` | `}` | block close |
| `⌁` | `\` | lambda |
| `▷` | `|>` | dispatch operator / arm introducer |
| `⇒` | `=>` | arm arrow |
| `⟲` | `~~` | cycle head |
| `↩` | `>>` | cycle arm mode: continue |
| `↯` | `<<` | cycle arm mode: finish |
| `•` | `::` | variant constructor/pattern separator |
| `⟦` | `[[` | map open |
| `⟧` | `]]` | map close |
| `↦` | `->` | map entry arrow |

## Additional ASCII aliases (for “pure ASCII” programs)

| Unicode token | ASCII alias(es) |
|---|---|
| `·` | `.` |
| `⋯` | `...` |
| `¬` | `!` |
| `∧` | `&&` |
| `∨` | `||` |
| `⊞` | `++` |
| `≤` | `<=` |
| `≥` | `>=` |
| `≠` | `!=` |
| `=` | `==` (optional) |
| `⊤` | `#t` |
| `⊥` | `#f` |
| `ø` | `#u` |

## Notes on equivalence

- The parser consumes the same token stream types for Unicode and ASCII. Internally, tokens are canonicalized to the Unicode form so downstream semantics (interpreter/VM) do not diverge.
- Error spans and caret diagnostics are anchored to the original source text (ASCII or Unicode), so location reporting remains correct.
