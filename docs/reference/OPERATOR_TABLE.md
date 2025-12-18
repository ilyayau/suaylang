# Operator table (v0.1)

This table is normative for parser precedence and associativity.

For full grammar, see [docs/GRAMMAR.md](../GRAMMAR.md).

## Precedence and associativity

Higher rows bind tighter.

| Level | Operators (Unicode) | ASCII aliases | Assoc | Notes |
|---:|---|---|:--:|---|
| 1 | `·` | `.` | left | Function application (curried) |
| 2 | `¬` | `!` | right | Unary not |
| 2 | unary `−` | unary `-` | right | Unary minus |
| 3 | `×` `÷` `%` | `*` `/` `%` | left | Multiplicative |
| 4 | `+` `−` | `+` `-` | left | Additive |
| 5 | `⊞` | `++` | left | Text concatenation |
| 6 | `=` `≠` `<` `≤` `>` `≥` | `==` `!=` `<` `<=` `>` `>=` | left | Comparisons |
| 7 | `∧` | `&&` | left | Short-circuit and |
| 8 | `∨` | `||` | left | Short-circuit or |
| 9 | `▷` (dispatch) | `|>` | left | Parses as an expression-level operator that introduces arms block |

Notes:

- `←`/`⇐` are not expression operators; they are top-level/block forms.
- `⇒` is not an operator; it is syntax inside `dispatch`/`cycle` arm headers.
