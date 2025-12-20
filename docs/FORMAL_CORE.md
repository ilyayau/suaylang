# Minimal Formal Core

## Subset Syntax (validated today)
- let-binding
- mutation
- pattern match
- cycle/state evolution
- error reporting (code, span)

## Formal Rules (big-step)

### Binding vs Mutation
1. let x = v in e ⟶ e[x ↦ v]
2. x := v ⟶ update x to v

### Dispatch / Pattern Branching
3. match v with {p1 → e1 | ...} ⟶ select branch by pattern

### Cycle / State Evolution
4. while c do e ⟶ repeat e while c true
5. state_machine {state, event → next_state} ⟶ transition by event

### Error Model
6. error(code, span) ⟶ observable outcome
7. error propagation: error in subexpr ⟶ error in parent
8. error(code, span) must match contract

## Observable Outcome
- Value equivalence: same value
- Error equivalence: same (error_code, span category)
- Ignore: message text, formatting
