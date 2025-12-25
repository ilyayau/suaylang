# Types

SuayLang is dynamically typed at runtime.

## Runtime value categories

- numbers (integers and decimals)
- strings
- booleans (`⊤`, `⊥`)
- unit (`ø`)
- tuples, lists, maps
- variants (tagged values)
- closures

## Guarantees

- Type errors are signaled with stable codes (docs/ERROR_CODES.md).
- No implicit coercions are performed unless explicitly defined by an operator.
