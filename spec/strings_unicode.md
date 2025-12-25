# Strings and Unicode

## Strings

- Strings are sequences of Unicode scalar values.
- Literal syntax is defined by the lexer (spec/lexical.md).

## Unicode operator surface

Unicode operator spellings are part of the surface syntax.
ASCII alternatives (if any) must be treated as syntactic sugar and must not change semantics.

## Determinism note

String comparison and concatenation use the host language’s deterministic semantics.
