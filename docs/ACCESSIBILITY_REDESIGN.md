# SuayLang Accessibility Redesign (Without High-Level Sugar)

This document proposes a redesign focused on **maximum accessibility** while preserving SuayLang’s defining property: **explicit, predictable execution**.

Constraints (non-negotiable):

- No new high-level abstractions.
- No convenience features that hide control flow.
- No exception-driven jumps.
- Favor explicitness and reversibility over brevity.

The goal is to make SuayLang understandable and usable by:

- beginners,
- systems programmers,
- people comfortable with assembly / bytecode / IR thinking,

…while keeping the language *honest* about what it does.

---

## 1) Dual-surface language model

### Single semantics, two surfaces
SuayLang keeps **one semantic core** (evaluation order, scoping rules, dispatch/cycle behavior). Two surfaces are just two ways to spell the same program:

- **Surface A — HUMAN-FRIENDLY**: readable and teachable, minimal cognitive overhead.
- **Surface B — MACHINE-EXPLICIT**: emphasizes state transitions and control decisions; close to bytecode/state-machine thinking.

Both surfaces compile/normalize to the same underlying token stream and have the same runtime behavior.

### Surface A: HUMAN-FRIENDLY
Surface A is optimized for first contact and code review.

Characteristics:

- Prefer ASCII forms (see §2) by default.
- Encourage “one decision per line” formatting in control-flow.
- Prefer explicit separators (newlines/commas) over adjacency tricks.
- Prefer variants for state machines (`State::payload`) over sentinel values.

It stays explicit. It just avoids “glyph shock” and reduces syntax memorization.

### Surface B: MACHINE-EXPLICIT
Surface B is optimized for reasoning like a compiler or VM.

Characteristics:

- Programs are written in a “control-first” style:
  - represent program state as data,
  - drive execution via `dispatch` and `cycle`,
  - avoid relying on operator precedence when clarity matters.
- Avoid implicit structure:
  - use parentheses,
  - avoid adjacency-separated tuple/list items,
  - keep all arms explicitly aligned.

Surface B is not a different language. It is a discipline: “write what you mean so a VM would approve.”

---

## 2) Official ASCII-friendly syntax layer (1-to-1, reversible)

### Principle
Every Unicode construct has exactly one ASCII spelling.

- **1-to-1**: each Unicode token maps to a single ASCII token string.
- **Reversible**: a lossless transform exists both directions.
- **Keyboard-safe**: only common ASCII characters and short keywords.

### Canonical mapping

The following table defines the *official* ASCII layer.

| Unicode | Meaning | ASCII | Notes |
|---|---|---|---|
| `⍝` | line comment | `#` | `# ...` to end-of-line |
| `⟪` | block open | `{|` | newline-separated forms |
| `⟫` | block close | `|}` | |
| `⟦` | map open | `{[` | map literal delimiter |
| `⟧` | map close | `]}` | |
| `←` | bind | `:=` | introduce name in current scope |
| `⇐` | mutate | `::=` | update existing name in nearest enclosing scope |
| `↦` | map entry | `->` | `key -> value` inside `{[ ]}` |
| `▷` | dispatch marker | `|>` | used both before the arm list and before each arm |
| `⇒` | arm arrow | `=>` | pattern-to-expression |
| `⟲` | cycle | `loop` | keyword token |
| `↩` | continue | `cont` | keyword token |
| `↯` | finish | `halt` | keyword token |
| `⌁` | lambda | `fn` | `fn(pattern ...) expr` |
| `·` | call | `@` | `f @ x @ y` |
| `•` | variant | `::` | `Tag::payload` |
| `⋯` | rest (pattern) | `...` | list patterns only |
| `ø` | unit | `unit` | literal |
| `⊤` | true | `true` | literal |
| `⊥` | false | `false` | literal |
| `¬` | not | `!` | prefix |
| `×` | multiply | `*` | infix |
| `÷` | divide | `/` | infix |
| `−` | minus | `-` | infix and unary |
| `⊞` | concat | `++` | infix; distinct from `+` |
| `≠` | not equal | `!=` | infix |
| `≤` | less/equal | `<=` | infix |
| `≥` | greater/equal | `>=` | infix |
| `∧` | and | `&&` | short-circuit |
| `∨` | or | `||` | short-circuit |

Notes:

- Existing ASCII fallbacks (`*`, `/`, `-`) remain valid; this table makes them **official and complete**.
- Keywords used here (`loop`, `cont`, `halt`, `fn`, `unit`, `true`, `false`) are reserved in the ASCII layer.

### Example: same program, Unicode vs ASCII

Unicode:

```suay
square ← ⌁(x) x × x
say · (text · (square · 7))
```

ASCII:

```suay
square := fn(x) x * x
say @ (text @ (square @ 7))
```

---

## 3) Core execution model (low-level, no hidden control)

SuayLang should be explained as “a tiny abstract machine with named environments.”

### 3.1 Values and environments
Execution operates on:

- **Values**: numbers, text, unit/bool, tuples/lists, maps, variants, closures, builtins.
- **Environments (scopes)**: frames mapping names to values, linked to a parent.

### 3.2 Evaluation is explicit and local
There is no implicit control transfer:

- Function application is explicit (`@` / `·`).
- Branching is explicit (`dispatch`).
- Looping is explicit (`cycle` / `loop`).
- Errors stop evaluation (no language-level catch/throw).

### 3.3 Control transitions are data-driven

#### Dispatch is a branch table over data shape
`dispatch` evaluates a scrutinee value, then checks arms top-to-bottom:

- Each arm match is a **decision point**.
- A match produces **bindings** (names in an arm scope).
- The arm body is evaluated in that scope.

Think of it like:

- assembly: a sequence of compares + conditional branches,
- bytecode: `MATCH` + `JUMP_IF_FAIL` over arms,
- IR: a multi-way branch with deconstruction.

#### Cycle is an explicit state machine
`cycle` (ASCII: `loop`) is the language’s “honest loop.” It is not a hidden `while`.

- It has an explicit **state value**.
- Each iteration is a `dispatch` on that state.
- Each arm chooses **cont** (continue with a new state) or **halt** (finish with a result).

This mirrors low-level control:

- assembly: loop header + state in registers + branch back edge,
- bytecode: a loop with a back-jump and an explicit state slot,
- IR/SSA: a loop with a state parameter and a $
  \phi
  $-like “next state” merge.

### 3.4 Relation to SSA / IR thinking
SuayLang is not SSA because it allows mutation (`::=` / `⇐`). But it supports an SSA-like *discipline*:

- Prefer `:=` bindings.
- Treat loop state as a single value threaded through `loop`.

In that style:

- each `:=` is like an SSA definition,
- each `dispatch` arm is a basic block with local bindings,
- each `loop` iteration is a controlled “next-state” computation.

---

## 4) CORE SUBSET (semantic core) and desugaring

### 4.1 Core subset
The core subset is the minimal set of constructs needed to express all SuayLang programs *without hiding control*.

Core constructs:

1) **Sequencing**
- Program order; blocks `{| ... |}` (Unicode `⟪ ⟫`).

2) **Names + scope operations**
- name reference
- bind `:=` (Unicode `←`)
- mutate `::=` (Unicode `⇐`)

3) **Functions**
- lambda `fn(...) expr` (Unicode `⌁`)
- call `@` (Unicode `·`)

4) **Data constructors**
- literals (`unit`, `true`, `false`, numbers, strings)
- tuples/lists/maps
- variants `Tag::payload` (Unicode `Tag•payload`)

5) **Control**
- `dispatch` via `|>` and arms `|> pat => expr`
- `cycle` via `loop seed |> {| arms |}` with `cont`/`halt`

6) **Primitive operators**
- unary `!`, unary `-`
- binary arithmetic, comparisons, `&&`, `||`, concat `++`

Everything else (formatting conveniences, stylistic sugar) should rewrite into this core.

### 4.2 Desugaring examples (Surface A → Core)

These are *syntactic* rewrites; semantics do not change.

#### A) Unicode → ASCII (lossless)

Unicode:

```suay
x ← 1
say · (text · x)
```

Core ASCII:

```suay
x := 1
say @ (text @ x)
```

#### B) “Implicit adjacency” → explicit separators
If a surface allows adjacency-separated tuple/list items, core style requires separators.

Surface A (adjacency tolerated):

```suay
t := (1 2 3)
xs := [1 2 3]
```

Core style (explicit separators):

```suay
t := (1
      2
      3)
xs := [1
       2
       3]
```

#### C) Cycle is already core, but it can be viewed as explicit tail recursion
This is not required, but it is useful for low-level reasoning.

Core `loop` form:

```suay
loop (State::s) |> {|
|> Done::x => halt x
|> State::s => cont (step @ s)
|}
```

Equivalent conceptual form (“tail recursion”):

```suay
run := fn(st)
  st |> {|
  |> Done::x  => x
  |> State::s => run @ (step @ s)
  |}

run @ (State::s)
```

This equivalence is a mental tool: it makes the loop’s control transfer explicit without adding any hidden behavior.

---

## 5) Mental model (how to think in SuayLang)

1) **Write programs as state transforms**
- Represent your program’s moving parts as data (often a variant).
- Use `dispatch` to decide what to do based on state shape.

2) **Treat `dispatch` as your “branch instruction”**
- Every arm is a deliberate control decision.
- Bindings live only inside the chosen arm.

3) **Treat `loop` as a state machine runner**
- One loop iteration = match the state, produce next state or final value.
- No implicit breaks; termination is an explicit `halt`.

4) **Prefer binding over mutation**
- Use `:=` for clarity.
- Use `::=` only when you truly want “update a cell in an enclosing scope.”

5) **Reason about correctness by enumerating states**
- If your loop state is a variant, correctness is “every state either progresses (`cont`) or terminates (`halt`).”
- If a dispatch has a `_` arm, treat it as a deliberate catch-all.

---

## 6) Side-by-side examples

Each example is shown in three views:

1) Surface A (readable)
2) Core Suay (explicit)
3) Bytecode-like pseudocode (conceptual)

### Example 1: Dispatch over variants

#### Surface A (Unicode)

```suay
classify ← ⌁(v)
  v ▷ ⟪
  ▷ Ok•x  ⇒ "ok:" ⊞ (text · x)
  ▷ Err•m ⇒ "err:" ⊞ m
  ▷ _     ⇒ "unknown"
  ⟫

say · (classify · (Ok•41))
```

#### Core Suay (ASCII)

```suay
classify := fn(v)
  v |> {|
  |> Ok::x  => "ok:" ++ (text @ x)
  |> Err::m => "err:" ++ m
  |> _      => "unknown"
  |}

say @ (classify @ (Ok::41))
```

#### Bytecode-like pseudocode

```text
# evaluate argument
PUSH 41
MAKE_VARIANT Ok

# call classify
LOAD classify
CALL 1

# inside classify(v):
#   MATCH v
#     case Ok(x):  return "ok:" ++ text(x)
#     case Err(m): return "err:" ++ m
#     default:     return "unknown"
MATCH v
  ARM Ok(x):
    PUSH "ok:"
    LOAD text; PUSH x; CALL 1
    CONCAT
    RETURN
  ARM Err(m):
    PUSH "err:"
    PUSH m
    CONCAT
    RETURN
  ARM _:
    PUSH "unknown"
    RETURN
```

### Example 2: Loop as a state machine (sum 1..n)

#### Surface A (Unicode)

```suay
sum_to ← ⌁(n)
  ⟲ (Step•(1 0)) ▷ ⟪
  ▷ Done•acc     ⇒ ↯ acc
  ▷ Step•(i acc) ⇒ ↩ (
      (i > n) ▷ ⟪
      ▷ ⊤ ⇒ Done•acc
      ▷ ⊥ ⇒ Step•(i + 1  acc + i)
      ⟫
    )
  ⟫

say · (text · (sum_to · 5))
```

#### Core Suay (ASCII)

```suay
sum_to := fn(n)
  loop (Step::(1 0)) |> {|
  |> Done::acc     => halt acc
  |> Step::(i acc) => cont (
       (i > n) |> {|
       |> true  => Done::acc
       |> false => Step::(i + 1  acc + i)
       |}
     )
  |}

say @ (text @ (sum_to @ 5))
```

#### Bytecode-like pseudocode

```text
# sum_to(n):
state = Step(i=1, acc=0)
LOOP:
  switch state.tag:
    Done:
      return state.acc
    Step:
      (i, acc) = state.payload
      if i > n:
        state = Done(acc)
      else:
        state = Step(i+1, acc+i)
      goto LOOP
```

### Example 3: Closure + explicit mutation (counter)

#### Surface A (Unicode)

```suay
make_counter ← ⌁(u) ⟪
  n ← 0
  ⌁(u2) ⟪
    n ⇐ n + 1
    n
  ⟫
⟫

c ← make_counter · ø
say · (text · (c · ø))
say · (text · (c · ø))
```

#### Core Suay (ASCII)

```suay
make_counter := fn(u) {|
  n := 0
  fn(u2) {|
    n ::= n + 1
    n
  |}
|}

c := make_counter @ unit
say @ (text @ (c @ unit))
say @ (text @ (c @ unit))
```

#### Bytecode-like pseudocode

```text
# make_counter():
#   allocate cell n in captured environment
#   return closure that increments that cell

n_cell = 0
return closure():
  n_cell = n_cell + 1
  return n_cell
```

---

## Summary

- The accessibility redesign is **syntax-first**, not feature-first.
- The ASCII layer is complete, reversible, and does not hide control flow.
- The execution model is best taught as a small abstract machine:
  - environments for scope,
  - dispatch for branching,
  - loop/cycle for state-machine iteration.
- The “core subset” is explicitly control-oriented and naturally aligns with bytecode/IR intuition.
