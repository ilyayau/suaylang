# SuayLang Reference Sheet (ASCII mapping, v0.1)

This file is an accessibility aid. It does not change SuayLang’s Unicode-first design.

## Compact ASCII mapping (proposed / partial)

| Unicode | ASCII | Meaning |
|---|---|---|
| `⌁` | `fn` (proposal) | lambda |
| `·` | `.` (proposal) | application |
| `←` | `<-` (proposal) | binding |
| `⇐` | `<=` (proposal) | mutation |
| `▷` | `match` (proposal) | dispatch |
| `⟲` | `loop` (proposal) | cycle |
| `↩` | `continue` (proposal) | cycle continue |
| `↯` | `break` (proposal) | cycle finish |
| `×` | `*` | multiply (currently accepted) |
| `÷` | `/` | divide (currently accepted) |
| `−` | `-` | minus (currently accepted) |

Notes:
- This table is intentionally conservative. Not all ASCII forms are implemented.
- See docs/ACCESSIBILITY_REDESIGN.md for the longer discussion and design constraints.
