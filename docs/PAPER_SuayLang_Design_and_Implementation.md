# SuayLang: Design and Implementation of an Explicit Control-Flow Language

(Full PDF content draft — text only)

## Abstract

SuayLang is a small programming language designed to make control flow explicit, composable, and mechanically understandable. Instead of statement-heavy constructs (e.g., `if/while/for`), SuayLang centers two expression-level primitives: `dispatch` (pattern matching) and `cycle` (a pattern-driven loop). The language is implemented in Python and provides both an interpreter (reference behavior) and a minimal stack-based bytecode virtual machine. This document describes the motivation behind SuayLang, its design philosophy, its core semantics and control constructs, its tooling and error model, and the implementation architecture. The goal is not to compete with production languages but to provide a constrained, reviewable design that is accessible to beginners while remaining legible to low-level programmers who think in terms of state machines, bytecode, and intermediate representations.

## 1. Introduction & Motivation

Most widely used languages expose control flow primarily through statement-oriented constructs such as `if`, `for`, `while`, and `switch`. These constructs are effective, but they often encourage patterns where the “shape” of control flow is distributed across syntactic forms that do not compose well as expressions. In practice, this frequently produces code where:

- control decisions cannot be easily nested into larger expressions,
- branching logic is written as ad-hoc boolean conditions instead of being tied to data shape,
- loops rely on implicit control mechanisms (`break`, `continue`, exceptions) that complicate local reasoning,
- state change is visually subtle (e.g., rebinding and mutation look similar).

SuayLang was created as a constraint-driven response to these issues. The motivating questions were:

1) Can a language remain small while still supporting non-trivial control flow?
2) Can branching and looping be expressed with a small number of primitives that have predictable evaluation behavior?
3) Can the resulting semantics be explainable both to beginners and to low-level programmers?

SuayLang’s answer is to emphasize **explicitness**:

- branching is `dispatch`, which matches on data shapes and binds names in arm-local scopes,
- looping is `cycle`, which repeatedly matches on an explicit state value and requires an explicit “continue vs finish” decision,
- state update is explicit via a distinct mutation operator,
- evaluation order is deterministic and visible in the syntax.

The language is intentionally limited. It does not attempt to provide large libraries, a complex module system, or an extensive ecosystem. Instead, it is built to be readable, reviewable, and teachable.

## 2. Language Design Philosophy

SuayLang is designed around a small number of principles.

### 2.1 Control flow should be expression-level and composable

In SuayLang, most constructs produce values. This aligns control flow with expression composition. Instead of writing “statement blocks that do not return a value,” SuayLang encourages writing expressions that compute results.

This design is not about concision; it is about locality. If branching is an expression, then it can be embedded into larger computations without introducing special-case syntax.

### 2.2 Data shape is a primary interface

SuayLang relies on a small set of data forms (numbers, text, tuples/lists, maps, variants). Variants (`Tag•payload`) provide a minimal sum-type mechanism, and patterns are used to deconstruct values.

The result is that branching decisions can often be written in terms of data shape rather than in terms of arbitrary predicates.

### 2.3 Mutation should be obvious

SuayLang distinguishes between introducing a name and updating an existing one:

- binding: `name ← expr`
- mutation: `name ⇐ expr`

This is a deliberate syntactic constraint. It does not remove mutation, but it ensures that state updates remain visible in code review.

### 2.4 Predictability is preferred over convenience

SuayLang avoids features that introduce hidden control transfer or complex desugaring. Examples of intentionally excluded features include:

- language-level exceptions with `try/catch`,
- implicit conversions across unrelated types,
- user-defined operators and precedence,
- concurrency primitives,
- macros or metaprogramming.

The objective is not minimalism for its own sake, but rather a semantic surface that remains comprehensible.

## 3. Core Semantics & Execution Model

This section describes how SuayLang evaluates programs.

### 3.1 Programs, expressions, and values

A SuayLang program is a sequence of expressions separated by newlines. Expressions are evaluated in order. Values include:

- numbers (integers and decimals)
- text
- unit (`ø`) and booleans (`⊤`, `⊥`)
- tuples and lists
- maps
- variants
- closures and builtins

Blocks `⟪ ... ⟫` contain newline-separated expressions and evaluate to the value of their last expression.

### 3.2 Deterministic evaluation order

Evaluation order is deterministic and can be reasoned about locally:

- binary operators evaluate left operand then right operand,
- function application evaluates the function expression then the argument expression,
- boolean operators `∧` and `∨` short-circuit,
- `dispatch` evaluates the scrutinee first and then checks arms in order,
- `cycle` evaluates the seed first and then iterates by matching the current state.

This determinism is critical for both beginner reasoning and low-level mapping.

### 3.3 Scoping and closures

SuayLang uses lexical scoping:

- a binding introduces a name in the current scope,
- a lambda closes over its defining environment,
- function calls create a new scope for parameters,
- selected `dispatch` and `cycle` arms create arm-local bindings.

Mutation updates the nearest enclosing scope containing the name.

### 3.4 Two execution paths

SuayLang includes two execution mechanisms:

1) **Interpreter** — the reference behavior for v0.1.
2) **Bytecode VM** — a stack-based compilation target intended to mirror the interpreter for the supported subset.

The interpreter defines the semantics. The VM exists both as a performance/engineering exercise and as a means to connect language semantics to lower-level execution models.

## 4. Control Flow Constructs (dispatch, cycle)

### 4.1 Dispatch: pattern-based branching

`dispatch` is written as:

```suay
value ▷ ⟪
▷ pattern ⇒ expr
▷ pattern ⇒ expr
⟫
```

Semantics:

1) Evaluate `value` to a scrutinee.
2) For each arm in order:
   - attempt to match `pattern` against the scrutinee,
   - if it matches, bind captured names in an arm-local scope and evaluate `expr` in that scope,
   - return the result of the first matching arm.
3) If no arm matches, raise a runtime error.

Patterns support wildcards, name bindings, literals, tuple/list structure (including list rest patterns), and variant patterns.

Dispatch is explicit control flow. It has no implicit fallthrough and no hidden jump mechanism.

### 4.2 Cycle: explicit state-machine looping

`cycle` is written as:

```suay
⟲ seed ▷ ⟪
▷ pattern ⇒ ↩ expr
▷ pattern ⇒ ↯ expr
⟫
```

Semantics:

1) Evaluate `seed` to an initial state value.
2) Repeat:
   - match the current state against arms in order,
   - for the first match:
     - if the arm uses `↩`, evaluate its expression to a new state and continue,
     - if the arm uses `↯`, evaluate its expression to a final result and terminate.
3) If no arm matches at any step, raise a runtime error.

Cycle enforces explicit termination: there is no implicit `break` or exception-driven jump.

### 4.3 Why these constructs

The combination of `dispatch` and `cycle` is intentionally small and orthogonal:

- `dispatch` provides structured branching on data shape.
- `cycle` provides structured looping by repeated matching on explicit state.

Together they cover much of what `if/switch` and `while/for` typically cover, but in a form that is amenable to expression composition and low-level reasoning.

## 5. Tooling & Error Model

### 5.1 Error categories

SuayLang reports errors in three categories:

- lexical errors
- syntax errors
- runtime errors

Errors are presented with file/line/column spans and caret context. This is a design requirement: errors should be understandable without reading implementation code.

### 5.2 No Python tracebacks as user experience

The CLI is designed to avoid exposing host-language exceptions. Unexpected internal failures are caught and reported as an internal error message rather than a Python traceback.

This constraint is enforced by stress tests that run the CLI and assert that output remains traceback-free.

### 5.3 Tooling-first posture

The repository includes:

- a CLI (`check`, `ast`, `run`)
- a minimal LSP server and a VS Code extension

The intent is to treat usability (diagnostics, hover help) as part of language quality.

## 6. Implementation Architecture

This section describes the structure at a system level.

### 6.1 Front-end

- Lexer: converts source text into tokens, preserving spans.
- Parser: recursive-descent parsing into an expression tree.

Newlines are significant in the grammar and influence parsing boundaries for programs and blocks.

### 6.2 Interpreter

The interpreter evaluates expressions directly:

- environments model lexical scope (a chain of frames),
- closures capture their defining environment,
- runtime errors attach spans and maintain a call stack.

Builtins provide the minimal standard library.

### 6.3 Bytecode compiler and VM

The compiler lowers expressions into a stack-based bytecode. The VM executes that bytecode with:

- an operand stack,
- an environment chain,
- explicit instructions for control, scope, and calls.

Pattern matching is supported in the VM via explicit match-related instructions, making `dispatch` and `cycle` visible as control flow in the instruction stream.

### 6.4 Testing strategy

The test suite includes:

- unit tests for lexer, parser, interpreter, modules, and stdlib
- stress tests focusing on robustness and “no tracebacks” requirements

The goal is reproducible evaluation behavior and stable diagnostic shape.

## 7. Lessons Learned & Future Work

### 7.1 Lessons learned

1) **Newlines as structure simplify some things and complicate others.**
   They reduce punctuation but require careful grammar rules and diagnostics.

2) **Pattern-driven looping is a strong constraint.**
   It forces explicit state representation, which improves local reasoning but demands discipline.

3) **Error spans matter as much as semantics.**
   Even a small language becomes hard to evaluate without precise diagnostics.

4) **Having a VM clarifies the semantics.**
   Lowering into bytecode exposes control decisions explicitly and provides a second lens on behavior.

### 7.2 Future work (non-commitments)

The v0.1 contract intentionally limits the scope. Reasonable future directions include:

- improved VM debug tables (PC-to-span mapping) and richer stack traces
- tighter interpreter/VM parity coverage
- module system formalization or compilation-aware module caching
- improved tooling integration (definitions, rename, formatting)

These are prospective areas, not promises.

---

## Appendix A: References inside this repository

- v0.1 language contract: `docs/LANGUAGE_CONTRACT_v0.1.md`
- formal grammar: `docs/GRAMMAR.md`
- semantics walkthrough: `docs/SEMANTIC_WALKTHROUGH.md`
- bytecode model: `docs/BYTECODE.md`
- minimal stdlib: `docs/STDLIB.md`
- design notes: `docs/WHY_SUAYLANG.md`
