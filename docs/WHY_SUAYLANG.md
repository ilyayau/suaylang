# What Makes SuayLang Unique (Design Notes)

SuayLang is not trying to be a “better Python” or “tiny JavaScript.” It’s a deliberately opinionated experiment in making **control flow** and **data shaping** feel like normal expressions, with the smallest surface area that still enables non-trivial programs.

This document is for engineers reviewing the language, not for users being sold on it.

## What problems SuayLang is designed to solve

### 1) Make control flow composable
In many mainstream languages, control flow is primarily statement-shaped: `if`, `for`, `while`, `switch`, early `return`, etc. That makes it awkward to:

- inline decisions inside larger expressions,
- build higher-order utilities without bolting on more syntax,
- represent “do this until it matches” patterns without bespoke loops.

SuayLang’s answer is:

- **Expression-first semantics**: most constructs produce values.
- **Pattern matching as a first-class control tool** via `dispatch`.
- **A single looping primitive** (`cycle`) that is pattern-driven instead of condition-driven.

The intent is that you can build programs out of **value transforms** and **pattern splits** instead of statement scaffolding.

### 2) Keep mutation explicit and rare
A lot of bugs are really “I changed something over here” bugs. SuayLang doesn’t prevent mutation, but it makes it visually loud:

- binding uses `←` (introduce a name)
- mutation uses `⇐` (update an existing name)

That separation is small, but it’s a real constraint: you can’t accidentally “re-bind” something and pretend it was an update (or vice versa). It pushes code toward immutable-by-default style without needing a static type system.

### 3) Treat data shape as the main interface
SuayLang’s core data model is minimal (numbers, text, tuples/lists, maps, variants), and the language leans on that:

- **Variants** (`Tag•payload`) are the primary sum-type mechanism.
- Patterns work across these shapes (including list “rest” patterns).

This makes it natural to model small protocols and structured results without classes, inheritance, or reflection.

## What SuayLang intentionally does NOT support

SuayLang’s constraints are the point. It intentionally does *not* include:

- **Classes / objects / inheritance**. There is no method dispatch, no field mutation, no OOP model.
- **User-defined operators** or custom precedence. The operator set is fixed.
- **Implicit type coercions**. Mixed-type arithmetic/comparison is rejected rather than “helpfully” converted.
- **Exceptions as a language feature**. Errors exist, but there’s no `try/catch` syntax in the language.
- **Concurrency / async** primitives.
- **Macros / metaprogramming**.
- **A large standard library**. Builtins are intentionally tiny.
- **A spec that promises implementation-independent behavior**. The current implementation is the reference.

If you want a language that grows features to match production ecosystems, SuayLang is the wrong project.

## How it differs from mainstream languages

### Dispatch-first instead of if/else chains
`dispatch` is pattern matching:

```suay
value ▷ ⟪
▷ Tag•x ⇒ x
▷ _     ⇒ 0
⟫
```

This replaces a mix of `switch`, destructuring, and some `if`/`else` usage. The key difference is that the *shape* of the data is the branching mechanism, not ad-hoc boolean conditions.

### Cycle: looping as pattern-driven state evolution
Instead of `while condition:` and separate `break/continue`, SuayLang uses:

- a **seed** value,
- a set of pattern arms,
- each arm chooses **continue** (`↩`) with a new state, or **finish** (`↯`) with a final value.

That makes a “loop” look like repeated evaluation of a state transformer. It’s closer to a small step evaluator than a control-flow statement.

### Application is a real operator (`·`) and functions are curried
Function application is `f · x · y`, not `f(x, y)`. Functions are naturally curried, which pushes APIs toward composable partial application and fits well with `map`/`fold`.

This is not syntactic novelty for its own sake: it’s a pressure toward writing libraries in terms of **pipelines of functions**, not “call this with five arguments.”

### Newlines are significant on purpose
SuayLang treats newlines as separators at the top level and inside blocks. This reduces punctuation noise (no semicolons), but it also makes layout part of the language.

It’s a constraint with benefits:

- blocks have a clear “sequence of forms” structure
- error spans are easier to anchor because expression boundaries are explicit

### Unicode operators are not a gimmick
The glyph-heavy syntax is intentionally compact and unambiguous:

- `←` vs `⇐` is visually distinct
- `▷`/`⇒` make pattern arms explicit
- `⟪ ⟫` visually fence blocks

ASCII fallbacks exist for some operators, but SuayLang is not trying to be friendly to every keyboard. The language is trying to be **readable once you know it**, not immediately familiar.

## Why the unconventional choices are justified

- **A small set of primitives is easier to reason about than a large set of partially-overlapping constructs.** `dispatch` + `cycle` cover a surprising amount of “business logic” control flow.
- **Explicit mutation is a design constraint that changes how code is written.** It’s not about purity; it’s about making state updates obvious.
- **Currying + `·` reduces API surface area.** With curried builtins, “multi-arg functions” don’t need special calling syntax.
- **Pattern-centric programming scales down well.** For small languages, patterns give you a lot of expressiveness without a full type system.

SuayLang is an experiment in *deliberate constraint*: remove features until what remains has a coherent shape.
