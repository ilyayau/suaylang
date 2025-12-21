# Formal Core

## Syntax (fragment)
- let x = e
- x := e
- if c then e1 else e2
- while c do e
- break v / continue v
- match e with {p -> e}
- state_machine {state, event -> next_state}
- error(code, span)

## Evaluation Rules (selected)

1. **Let binding:**
   (let x = v in e) ⇓ e[x ↦ v]
2. **Mutation:**
   (x := v; e) ⇓ e, with x updated
3. **If-expression:**
   if true then e1 else e2 ⇓ e1
   if false then e1 else e2 ⇓ e2
4. **While loop:**
   while false do e ⇓ unit
   while true do e ⇓ (e; while c do e)
5. **Break/Continue:**
   break v exits loop with value v
   continue v skips to next iteration
6. **Match:**
   match v with {p -> e} ⇓ e if v matches p
7. **State machine:**
   state_machine {s, e -> s'} steps by event
8. **Error:**
   error(code, span) halts with error

## Observation Policy (normative)
- Only value, error (code+span), and stdout are observable.
- Message text and formatting are ignored.
- Non-deterministic output is not allowed.

## Out of Scope
- Side effects beyond stdout
- Non-deterministic behaviors
- External I/O
