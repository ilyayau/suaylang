# Error codes (stable contract)

This catalog defines stable diagnostic codes.

- The **code** is stable in v0.1.x.
- The **human message** may evolve as long as the code and span policy remain stable.

## E-LEX — Lexical error

- **Category:** lex
- **Meaning:** The input cannot be tokenized (unexpected character, unterminated literal, etc.)
- **Span policy:** caret at the problematic character.

## E-ESC — Invalid escape sequence

- **Category:** lex
- **Meaning:** Unknown or malformed escape in a string literal.

## E-SYNTAX — Syntax error

- **Category:** syntax
- **Meaning:** The token stream cannot be parsed into a program.
- **Span policy:** caret at the parser’s current token (EOF for missing terminator).

## E-NAME — Name error

- **Category:** runtime
- **Meaning:** Undefined name, duplicate binding in a scope, or mutation of an unbound name.

## E-NOMATCH — No pattern match

- **Category:** runtime
- **Meaning:** No `dispatch` arm (or `cycle` arm) matched.

## E-TYPE — Type error

- **Category:** runtime
- **Meaning:** An operator/builtin was applied to values of the wrong runtime type.

## E-DIV0 — Division by zero

- **Category:** runtime
- **Meaning:** Division by zero occurred in numeric operators.

## E-STACK — Stack overflow / recursion limit

- **Category:** runtime
- **Meaning:** Recursion exceeded the implementation’s recursion limit.

## E-IMPORT — Module load failure

- **Category:** runtime
- **Meaning:** A module could not be loaded (filesystem/permission/etc).

## E-IMPORT-CYCLE — Module import cycle

- **Category:** runtime
- **Meaning:** A cycle was detected in module loading.

## E-RUNTIME — Generic runtime error

- **Category:** runtime
- **Meaning:** Runtime error not yet assigned a more specific stable code.

## E-UTF8 — Invalid UTF-8 source file

- **Category:** IO/host
- **Meaning:** Source file cannot be decoded as UTF-8.

## E-FEATURE-NOT-IN-V1 — Feature gated / not in v1

- **Category:** runtime
- **Meaning:** A program used syntax or behavior that is intentionally excluded from the current language version contract.
- **Span policy:** caret at the first token that requires the gated feature.

---

## W-* warnings

Warnings are reserved for non-fatal diagnostics. v0.1 currently treats warnings as tooling-only.

- `W-SHADOW` — Shadowing detected (reserved)

- `W-UNICODE-SYNTAX` — Unicode spelling used (tooling-only)
	- Emitted when a source file uses Unicode operator spellings where ASCII is canonical.
	- Warnings are non-fatal and may be enabled/disabled by tooling.

- `W-SHADOW` — Shadowing detected (reserved)
