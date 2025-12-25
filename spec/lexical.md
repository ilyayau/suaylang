# Lexical rules

This document separates lexical rules from syntax.

## Source encoding

- Source files are UTF-8.
- Unicode operator spellings are permitted as part of the language surface.

## Tokens

The lexer produces:

- IDENT
- INT / DEC
- STRING
- punctuation and operator tokens used in the grammar
- NEWLINE and EOF

## Comments

- `#` introduces a comment to end-of-line, except where it is part of a boolean/unit literal token (implementation detail).

## Strings

- Strings use escape sequences defined by the lexer.
- Invalid escapes are lexical errors.
