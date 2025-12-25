# Evaluation order

This document defines a deterministic evaluation order.

## Core rule

Evaluation proceeds left-to-right at each syntactic construct unless otherwise stated.

## Specific constructs

- Binary operators: evaluate left operand, then right operand, then apply operator.
- Short-circuit AND/OR (`∧`/`∨`):
  - `a ∧ b`: evaluate `a`; if falsey, result is `a` (or false); else evaluate `b`.
  - `a ∨ b`: evaluate `a`; if truthy, result is `a` (or true); else evaluate `b`.
- Call (`·`): evaluate callee expression first, then argument expression, then apply.
- Map literals: evaluate key expression then value expression for each entry in source order.
- Block (`⟪ ... ⟫`): evaluate items in order; the block result is the value of the last item.
- Dispatch/cycle arms are tested in textual order.
