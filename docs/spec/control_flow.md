# SuayLang control-flow spec (minimal, v0.1)

This document is a **minimal, test-backed** specification for SuayLang’s core control-flow constructs.
It aims to be precise enough for interpreter/VM equivalence, while staying aligned with the implementation.

## Dispatch (`▷`)

Surface form:

- `value ▷ ⟪ ▷ pat ⇒ expr ... ⟫`

Semantics:

- Evaluate `value` once to obtain the **scrutinee**.
- Arms are checked **top-to-bottom**.
- The **first arm** whose pattern matches the scrutinee is selected.
- Pattern variables bind in a fresh environment for the selected arm only.
- If no arm matches, raise a runtime error: `No dispatch arm matched`.

Observables:

- Deterministic arm selection.
- No side effects from non-selected arms.

## Cycle (`⟲`)

Surface form:

- `⟲ seed ▷ ⟪ ▷ pat ⇒ ↩ expr | ▷ pat ⇒ ↯ expr ... ⟫`

Semantics:

- Evaluate `seed` once to obtain the initial **state**.
- Repeat:
  - Match `state` against the arms **top-to-bottom**.
  - For the first matching arm, evaluate the arm expression in an environment extended with its bindings.
  - If the arm is marked `↩` (**continue**):
    - set `state` to the arm value and loop.
  - If the arm is marked `↯` (**finish**):
    - return the arm value and stop.
- If no arm matches, raise a runtime error: `No cycle arm matched`.

Notes:

- `↩` / `↯` are only valid in the **cycle arm mode** position.

## Binding vs mutation

- Binding (`name ← expr`) introduces a new name in the current environment.
- Mutation (`name ⇐ expr`) updates an existing binding (searching outward through lexical parents).
  - If the name is not already defined, it is a runtime error.

## Scope rules (lexical)

- Blocks and dispatch/cycle arms evaluate with fresh environments that have the surrounding environment as parent.
- Lambdas capture their defining environment (closures).
