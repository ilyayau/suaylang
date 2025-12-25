# Scopes and environments

SuayLang uses lexical environments.

## Bindings

- `x ← e` evaluates `e` and defines `x` in the current environment.
- `x ⇐ e` evaluates `e` and updates the nearest enclosing environment where `x` is bound; otherwise it is an error.

## Blocks

- A block `⟪ e1 ... en ⟫` creates a child environment for its body.
- Bindings inside a block do not escape the block environment.

## Lambdas

- A lambda captures the environment at its definition site.
- Parameter bindings are introduced in the lambda’s call environment.

## Pattern-binding

- When a pattern match succeeds in dispatch/cycle, bindings introduced by the pattern are added in a fresh child environment for the arm body.
