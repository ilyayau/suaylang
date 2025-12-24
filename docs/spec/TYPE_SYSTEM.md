# Type system (v0.1)

SuayLang v0.1 is dynamically typed.

Normative reference: docs/LANGUAGE_REFERENCE.md.

## Runtime value categories

- Unit, Bool, Int, Dec (float), Text (string)
- Tuple, List, Map
- Variant (tagged value)
- Closure / Builtin

## Type errors

- Operators and builtins have runtime type requirements.
- Violations raise E-TYPE (see docs/ERROR_CODES.md).

## Coercions

- Truthiness is defined for control constructs (see docs/LANGUAGE_REFERENCE.md).
- No implicit numeric coercions are specified beyond host Python semantics for int/float operations.
