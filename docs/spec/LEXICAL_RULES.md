# Lexical rules (v0.1)

Normative references:

- docs/LANGUAGE_REFERENCE.md (source text + canonical ASCII)
- docs/ASCII_SYNTAX.md (ASCII spellings)
- suaylang/lexer.py (implementation)

## Source encoding

- Source files are UTF-8 text.
- If a file cannot be decoded as UTF-8, the CLI fails with E-UTF8.

## Whitespace and newlines

- Spaces, tabs, and carriage returns are treated as separators.
- NEWLINE tokens are significant as separators between top-level forms and block forms.

## Comments

Supported line comments (to end-of-line; newline itself remains tokenized):

- Unicode: ⍝ ...
- ASCII canonical: // ...
- Compatibility: # ... (accepted by the lexer for baseline compatibility; does not apply to #t/#f/#u literals)

## Identifiers

- Identifiers are Unicode-letter-based with '_' support (see docs/GRAMMAR.md and lexer implementation).

## Literals

- Unit: #u (alias ø)
- Booleans: #t/#f (aliases ⊤/⊥)
- Integers: INT
- Decimals: DEC (Python float)
- Strings: "..." with escapes \n, \t, \", \\ (no raw newlines)
