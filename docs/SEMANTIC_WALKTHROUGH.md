# SuayLang Semantic Walkthrough (v0.1)

This document explains **how SuayLang evaluates programs**: evaluation order, scope creation/destruction, and the control-flow semantics of `dispatch` and `cycle`.

No implementation details are used here (no AST/bytecode/parsing internals). This is purely a language-semantics walkthrough.

## Mental model: evaluation + scopes

### Evaluation is expression-first
A SuayLang program is a sequence of **expressions**. Each expression evaluates to a **value**.

At the top level (and inside blocks), expressions are evaluated **in order**. The last evaluated expression is the “result” of that sequence (blocks return the last expression’s value).

### Deterministic evaluation order
When an expression contains subexpressions, evaluation is deterministic and generally **left-to-right**:

- For `a + b`, evaluate `a`, then evaluate `b`, then apply `+`.
- For `f · x`, evaluate `f`, then evaluate `x`, then apply.
- For `¬e` or `−e`, evaluate `e`, then apply the unary operator.
- For `a ∧ b` / `a ∨ b`, `a` is evaluated first and may short-circuit.

### Scopes (environments)
You can think of scopes as a stack of frames that map names to values.

- **Top-level scope** exists for the duration of the program.
- A **block** `⟪ ... ⟫` introduces sequencing (and typically a fresh nested scope in the semantic model).
- A **lambda call** creates a new scope for its parameters and locals, with a parent scope captured when the lambda was created.
- A **dispatch arm** creates a new scope that contains the pattern bindings for that arm.
- A **cycle arm** likewise creates a new scope with pattern bindings for that step.

### Binding vs mutation
- `name ← expr` **binds** a name in the current scope.
- `name ⇐ expr` **updates** an existing binding in the nearest enclosing scope that already contains `name`.

That distinction is part of the semantics: mutation is not “re-binding.”

---

## Program 1 — Closures + lexical scope + explicit mutation

This program builds a counter function that remembers state across calls.

### Source

```suay
make_counter ← ⌁(u) ⟪
  n ← 0
  ⌁(u2) ⟪
    n ⇐ n + 1
    n
  ⟫
⟫

c ← make_counter · ø

a ← c · ø
b ← c · ø

say · (text · a)
say · (text · b)
```

### Walkthrough

1) **Top-level: define `make_counter`**
- `⌁(u) ...` evaluates to a function value (a closure).
- That closure captures the current top-level scope as its parent (lexical scoping).
- `make_counter ← <closure>` binds the name `make_counter` in the top-level scope.

2) **Call `make_counter` to produce a counter**
- `c ← make_counter · ø`
  - Evaluate `make_counter` to the closure.
  - Evaluate `ø` to the unit value.
  - Apply the closure to the argument:
    - Create a new scope `S_make_counter_call` for parameter `u`.
    - Evaluate the body block `⟪ ... ⟫` in that scope.

3) **Inside `make_counter` body: create local state and return an inner function**
- `n ← 0`:
  - Evaluate `0`.
  - Bind `n` in `S_make_counter_call`. This is the counter’s private state.
- Next expression is a lambda: `⌁(u2) ⟪ ... ⟫`
  - Evaluates to a closure that captures **`S_make_counter_call`** (so it can see `n`).
- The block returns that inner closure as its final value.
- The call finishes; `c` is bound at top level to that returned closure.

4) **First call: `a ← c · ø`**
- Evaluate `c` to the inner closure.
- Evaluate `ø`.
- Apply:
  - Create a new scope `S_c_call_1` for parameter `u2`, whose parent is the captured scope `S_make_counter_call`.
  - Evaluate the inner block:
    - `n ⇐ n + 1`
      - Evaluate `n` by searching scope chain: not in `S_c_call_1`, found in `S_make_counter_call`.
      - Evaluate `1`.
      - Compute `n + 1`.
      - Mutate: update `n` in `S_make_counter_call`.
    - Evaluate `n` again; it now yields the updated value.
  - The block returns the updated `n`.
- Bind `a` at top level to that returned number.

5) **Second call: `b ← c · ø`**
- Same as step 4, but now `n` starts from the already-updated value (because the closure kept `S_make_counter_call`).
- So `b` becomes `a + 1`.

6) **Printing**
- `say · (text · a)`:
  - Evaluate `say` builtin, then evaluate argument `(text · a)`.
  - `(text · a)` evaluates `text`, then `a`, then converts to a `Text` value.
  - `say` prints that text.

### Scope lifecycle summary
- Top-level scope: lives for the whole program.
- `S_make_counter_call`: created when calling `make_counter`; **kept alive** because `c`’s closure captures it.
- `S_c_call_1` and `S_c_call_2`: created per call to `c`; destroyed after each call finishes.

---

## Program 2 — `dispatch`: pattern matching and arm scopes

This program classifies a value shaped as a variant and returns a text result.

### Source

```suay
classify ← ⌁(v)
  v ▷ ⟪
  ▷ Ok•x   ⇒ "ok:" ⊞ (text · x)
  ▷ Err•m  ⇒ "err:" ⊞ m
  ▷ _      ⇒ "unknown"
  ⟫

say · (classify · (Ok•41))
say · (classify · (Err•"bad"))
say · (classify · (Ok•(1 2)))
```

### Walkthrough

1) **Define `classify`**
- `classify ← ⌁(v) ...` binds a closure in the top-level scope.

2) **Evaluate `say · (classify · (Ok•41))`**
- Evaluate `say`.
- Evaluate `(classify · (Ok•41))`:
  - Evaluate `classify`.
  - Evaluate `(Ok•41)`:
    - Evaluate `41`.
    - Construct the variant value `Ok•41`.
  - Apply `classify` to that variant:
    - Create a new scope for parameter `v`.
    - Evaluate the body, which is a `dispatch`.

3) **Dispatch evaluation order**
For `v ▷ ⟪ ... ⟫`:

- Evaluate the scrutinee expression `v` to a value.
- Consider arms **top-to-bottom**:
  - For each arm, attempt to match the pattern against the scrutinee value.
  - On the first match:
    - Create a fresh **arm scope** containing the bindings produced by the pattern.
    - Evaluate the arm expression in that scope.
    - The dispatch expression returns that arm’s result.

4) **Arm 1 matches and binds `x`**
- Pattern `Ok•x` matches the variant `Ok•41`.
- Binding: `x` is bound to `41` in the arm scope.
- Evaluate arm expression: `"ok:" ⊞ (text · x)`
  - Evaluate left text literal.
  - Evaluate `(text · x)`:
    - Evaluate `text`, then `x` (found in the arm scope), convert to text.
  - Apply concatenation `⊞`.
- Return the concatenated `Text` from `classify`.

5) **Outer `say` prints the result**
- `say` receives the text and prints.

6) **Second call: `Err•"bad"`**
- The first arm fails (`Ok•...` does not match).
- The second arm `Err•m` matches and binds `m` to `"bad"`.
- That arm returns `"err:" ⊞ m`.

7) **Third call: `Ok•(1 2)`**
- `Ok•x` matches; `x` is bound to the tuple `(1 2)`.
- `text · x` converts the tuple to text.

### Scope lifecycle summary
- Each `classify` call creates a parameter scope.
- Each matching arm creates an arm scope that exists only while evaluating that arm.
- Pattern bindings (`x`, `m`) do not “leak” outside the selected arm.

---

## Program 3 — `cycle`: looping as repeated pattern-driven state

This program computes the sum `1 + 2 + ... + n` using `cycle`. The loop state is a variant:

- `Step•(i acc)` means “continue with index `i` and accumulator `acc`.”
- `Done•acc` means “finish and return `acc`.”

### Source

```suay
sum_to ← ⌁(n)
  ⟲ (Step•(1 0)) ▷ ⟪
  ▷ Done•acc      ⇒ ↯ acc
  ▷ Step•(i acc)  ⇒ ↩ (
      (i > n) ▷ ⟪
      ▷ ⊤ ⇒ Done•acc
      ▷ ⊥ ⇒ Step•(i + 1  acc + i)
      ⟫
    )
  ⟫

say · (text · (sum_to · 5))
```

### Walkthrough

1) **Call `sum_to · 5`**
- Evaluate `sum_to`, evaluate `5`, apply:
  - Create a scope for parameter `n` bound to `5`.
  - Evaluate the `cycle` expression.

2) **Cycle initializes state**
- Evaluate the seed expression `(Step•(1 0))`:
  - Evaluate tuple `(1 0)`.
  - Wrap as variant `Step•(1 0)`.
- That value becomes the initial cycle state.

3) **Cycle step: choose an arm by pattern matching**
`⟲ state ▷ ⟪ arms ⟫` repeats:

- Match the current state against arms top-to-bottom.
- If the chosen arm uses `↩ expr`, evaluate `expr` to a **new state** and repeat.
- If the chosen arm uses `↯ expr`, evaluate `expr` to the **final result** and stop.

4) **First iteration (state = `Step•(1 0)`)**
- Arm 1: `Done•acc` does not match.
- Arm 2: `Step•(i acc)` matches.
  - Create a cycle-arm scope binding `i = 1`, `acc = 0`.
  - Evaluate the arm’s continue expression `↩ (...)`.

5) **Nested decision inside the cycle arm**
The continue expression is a `dispatch` on `(i > n)`:

- Evaluate `(i > n)` in the cycle-arm scope:
  - Evaluate `i` (1), evaluate `n` (5 from the outer function scope), compute `1 > 5` → `⊥`.
- Dispatch on that boolean:
  - `▷ ⊤ ⇒ ...` does not match.
  - `▷ ⊥ ⇒ Step•(i + 1  acc + i)` matches.
- Evaluate `Step•(i + 1  acc + i)`:
  - Compute `i + 1` → 2.
  - Compute `acc + i` → 1.
  - Construct tuple `(2 1)` and wrap as `Step•(2 1)`.
- The cycle continues with new state `Step•(2 1)`.

6) **Repeat until termination**
Eventually, when `i` becomes `6`, the nested dispatch sees `i > n` as `⊤` and returns `Done•acc`.

7) **Final iteration (state = `Done•acc`)**
- Arm 1 matches: `Done•acc ⇒ ↯ acc`.
- Bind `acc` in the cycle-arm scope.
- Evaluate `acc` and finish the cycle with that value.

8) **Print result**
- `text · (sum_to · 5)` converts the resulting number to text.
- `say` prints it.

### Scope lifecycle summary
- `sum_to` call scope holds `n`.
- Each cycle iteration creates a fresh arm scope (`i`, `acc` bindings) for the selected arm.
- The nested dispatch creates an additional short-lived arm scope (though here it introduces no new names).
- Cycle terminates when an arm chooses `↯`.

---

## Takeaways

- SuayLang semantics push control flow into **value-producing expressions**.
- `dispatch` is the primary branching tool; pattern bindings are scoped to the chosen arm.
- `cycle` is a loop defined as **repeated pattern matching on a state value**, not a condition-driven statement.
- Closures + explicit mutation (`⇐`) allow stateful abstractions, but make state updates obvious.
