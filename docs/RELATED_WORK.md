# Related Work (design-relevant, bullet-level)

- Rust: both support pattern matching over structured data; SuayLang makes branching and looping expression-shaped primitives (`dispatch`/`cycle`) rather than mixing expressions with statement-oriented control constructs.
- Haskell: both support pattern matching and higher-order programming; SuayLang uses an explicit state-transition loop (`cycle`) instead of relying on recursion as the default looping mechanism.
- OCaml: both use algebraic-data-style variants and pattern matching; SuayLang’s `cycle` couples pattern matching with explicit continue/finish modes to represent state machines directly.
- Erlang: both encourage modeling control flow via tagged values (success/error variants); SuayLang is a single-process, deterministic semantics experiment rather than a concurrent fault-tolerant runtime.
- Scheme/Racket: both treat many constructs as expressions; SuayLang restricts metaprogramming (no macros) to keep the semantic surface small and testable.
- Lua: both emphasize a small core and embedding-friendly implementation; SuayLang’s evaluation focus is differential validation of two backends rather than an extensible production ecosystem.
- WebAssembly (Wasm): both use a compact instruction model for execution; SuayLang’s VM is validated against a reference interpreter for a subset, whereas Wasm standardizes the bytecode as the primary specification target.
- Forth: both can be understood as small-core languages with explicit execution models; SuayLang uses lexical scoping, closures, and structured pattern matching rather than stack-manipulation as the programmer-facing abstraction.
- Elm: both restrict features to preserve predictability; SuayLang’s constraints are aimed at semantic checkability and backend equivalence evidence, not at UI architecture.
- Smalltalk: both can treat computation as value-producing expressions; SuayLang does not use an object/message model and instead centers on data shape (variants/lists/tuples) plus pattern matching.
