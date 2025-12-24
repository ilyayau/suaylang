# Scoping rules (v0.1)

Normative reference: docs/LANGUAGE_REFERENCE.md.

## Lexical scoping

- Blocks introduce a new lexical environment.
- Lambdas capture the lexical environment at definition time (closures).

## Binding and mutation

- Binding (<-) introduces a new name in the current scope; rebinding in the same scope is E-NAME.
- Mutation (<~) updates the nearest enclosing scope that already contains the name; mutating an unbound name is E-NAME.

## Shadowing

- Inner scopes may shadow outer bindings; lookup uses the innermost binding.
