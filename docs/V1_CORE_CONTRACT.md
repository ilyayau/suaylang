# SuayLang v1 core contract (normative)

This document freezes the **v1 core semantics** that are treated as stable and tested.
It is intentionally short: it is the contract that contract tests enforce.

Scope:

- Core expressions (literals, lists/tuples/maps, lambdas, application, blocks)
- Binding (`<-`) and mutation (`<~`)
- Control-flow expressions: `dispatch` (`|>`) and `cycle` (`~~`, `>>`, `<<`)
- Error model: phases + spans + stable error codes
- Determinism (within the stated assumptions)

Non-goals (not covered by this contract): module system semantics, LSP behavior, formatter stability beyond ASCII-first guarantees, performance guarantees.

## Evaluation order

SuayLang is strict (eager) except for short-circuit operators.

1) **Block order**

- A block `{ e1; e2; ...; en }` evaluates expressions **top-to-bottom**.
- The block result is the value of the last expression `en`.

2) **Function application**

- In `f . a . b` (application is left-associative), evaluation is:
  - evaluate `f`, then `a`, then apply; then evaluate `b`, then apply, etc.

3) **Composite literals**

- Tuple `(e1 e2 ... en)`, List `[e1 e2 ... en]`, and Map `[[k1 -> v1  k2 -> v2 ...]]` evaluate their element expressions **left-to-right**.

4) **Operators**

- Unary operators evaluate their operand.
- Binary operators evaluate **left operand, then right operand**, except:
  - `&&` and `||` are **short-circuiting** (right operand is evaluated only if needed).

## Scoping and shadowing

1) **Lexical scope**

- Names are resolved lexically: a reference to `x` uses the **nearest enclosing** binding of `x`.

2) **Block scope**

- A block introduces a new scope.
- Bindings created with `<-` inside a block are not visible outside that block.

3) **Shadowing**

- Binding a name that already exists in an outer scope is allowed (shadowing).
- Within the inner scope, the inner binding is the one that is referenced and mutated.

## Binding vs mutation

SuayLang distinguishes creating a binding from updating one.

1) **Binding (`<-`)**

- `x <- e` evaluates `e` then binds the resulting value to `x` in the **current scope**.
- Re-binding `x` in the same scope is a runtime error (see error model).

2) **Mutation (`<~`)**

- `x <~ e` evaluates `e` then updates an **existing** binding of `x`.
- The binding that is mutated is the nearest enclosing binding of `x`.
- Mutating a name that is not bound in any enclosing scope is a runtime error.

## Error model (phases, codes, spans)

All user-facing failures are classified into one of these phases:

- **Lex**: tokenization/lexical errors (`E-LEX`, `E-ESC`, ...)
- **Parse**: syntax errors (`E-SYNTAX`)
- **Runtime**: dynamic errors during evaluation (`E-NAME`, `E-TYPE`, `E-DIV0`, `E-NOMATCH`, ...)

Stability guarantees:

- Errors have a stable **error code** (see [docs/ERROR_CODES.md](docs/ERROR_CODES.md)).
- Errors include a stable **source span**:
  - Lex/parse errors: `(line, column)` points at the offending token/location.
  - Runtime errors: `(line, column)` points at the expression/operator that triggered the error.

Contract tests assert **(code, line, column)** exactly for invalid programs.

## `dispatch` semantics (`|>`)

Syntax shape (ASCII):

```suay
scrutinee |> {
|> pattern1 => expr1
|> pattern2 => expr2
|> _        => exprN
}
```

Semantics:

- The scrutinee expression is evaluated **exactly once** to a value `v`.
- Arms are tried **top-to-bottom**.
- The first arm whose pattern matches `v` is selected; its pattern binders are bound for the arm body evaluation.
- If no arm matches, evaluation raises runtime error `E-NOMATCH` with a span at the `dispatch` expression.

## `cycle` semantics (`~~`, `>>`, `<<`)

`cycle` is an explicit state-machine loop.

Syntax shape (ASCII):

```suay
~~ (initial_state) |> {
|> Done::x => << x
|> Step::s => >> next_state_expr
}
```

Semantics:

- The `initial_state` expression is evaluated once to a value `state`.
- The arms behave like `dispatch`, matching on the current `state`.
- The selected arm body must evaluate to either:
  - `<< value`: terminate the cycle and return `value`
  - `>> state2`: continue the cycle with new state `state2`
- If no arm matches the current state, evaluation raises runtime error `E-NOMATCH`.

## Determinism guarantees

Given:

- identical source text,
- the same SuayLang version,
- the same module search/filesystem contents (if modules are used),
- and no use of interactive input (`hear`) or external side effects,

then evaluation is deterministic:

- the returned value and the produced stdout are the same on repeated runs.

Contract tests enforce determinism by running each case twice per backend.
