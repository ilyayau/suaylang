# Supported subset for interpreter↔VM equivalence (v0.1)

This document defines the subset for which SuayLang makes an **interpreter↔VM observational equivalence** claim.

**Definition (operational):** the subset is the set of programs whose AST uses only constructs supported by the compiler+VM in v0.1.

## Subset constructs (expressions)

- Literals: `ø`, `⊤/⊥`, integers, decimals, text
- Names (identifier references)
- Binding (`←`) and mutation (`⇐`)
- Block (`⟪ ... ⟫`) with newline-separated forms
- Tuples `(a b ...)`
- Lists `[a b ...]`
- Maps `⟦ k ↦ v, ... ⟧`
- Variants `Tag•payload`
- Lambdas / closures `⌁(p1 p2 ...) expr`
- Application `f · x` (curried)
- Unary operators (e.g., `¬`)
- Binary operators (arithmetic, comparison, boolean `∧/∨`, concat `⊞`)
- `dispatch` (pattern matching): `value ▷ ⟪ ▷ pat ⇒ expr ... ⟫`
- `cycle` (pattern-driven loop): `⟲ seed ▷ ⟪ ▷ pat ⇒ ↩ expr | ▷ pat ⇒ ↯ expr ... ⟫`

## Subset patterns

- `_` wildcard
- Name binder patterns (e.g., `x`)
- Literal patterns: `ø`, `⊤/⊥`, numbers, text
- Tuple patterns: `(p q ...)`
- List patterns: `[]`, `[p q ...]`, and rest-tail form `[p q ⋯xs]` where tail is a name or `_`
- Variant patterns: `Tag•p`

## Explicitly out of scope (for equivalence claims)

- Modules via `link` (interpreter-only in v0.1)
- Any interpreter feature not implemented by the compiler/VM
- Interactive input (`hear`) unless a deterministic harness provides it

## Why this subset is intentionally limited

The goal is to make H2 falsifiable with automatic checks. A narrow, explicit subset:

- makes divergences actionable (each counterexample is within a known construct set), and
- avoids inflating claims to features that the VM does not implement.
