# Error catalog (legacy draft)

Canonical error code catalog:

- [docs/ERROR_CODES.md](../ERROR_CODES.md)

This catalog defines stable error codes `E0001`… used by contract-mode tooling and golden diagnostics.

Important:

- v0.1 default diagnostics remain human-readable.
- Tooling may include codes when enabled (e.g., `suay explain E0001`).
- The *code* is stable; the exact message wording may evolve in v0.1.x.

## E0001 — Unexpected character (lexer)

- **Category:** lex
- **Template:** `Unexpected character <ch>`
- **Span policy:** caret at the unexpected character.

Example:

```text
1:1: lex error: Unexpected character '@'
@
^
```

## E0002 — Unknown string escape (lexer)

- **Category:** lex
- **Template:** `Unknown string escape \\<esc>`

## E0101 — Syntax error (parser)

- **Category:** syntax
- **Template:** `Expected ...`

## E0102 — Maximum parse depth exceeded

- **Category:** syntax
- **Template:** `Maximum parse depth exceeded`

## E0201 — Undefined name (runtime)

- **Category:** runtime
- **Template:** `Undefined name <name>`

## E0202 — Duplicate binding in scope (runtime)

- **Category:** runtime
- **Template:** `Name <name> is already bound in this scope`

## E0203 — Mutation of unbound name (runtime)

- **Category:** runtime
- **Template:** `Cannot mutate <name>: name is not bound in any enclosing scope`

## E0204 — No dispatch arm matched (runtime)

- **Category:** runtime
- **Template:** `No dispatch arm matched`

## E0205 — No cycle arm matched (runtime)

- **Category:** runtime
- **Template:** `No cycle arm matched`
