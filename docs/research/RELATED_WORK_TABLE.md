# Related work table

| System | Similarity | Difference | Why it matters to our hypothesis |
|---|---|---|---|
| Rust | Pattern matching over structured data | `match` is statement-like in some contexts; broader type system/ecosystem | Helps frame `dispatch` as a minimal match primitive, not a full ML-style system |
| OCaml | Variants + pattern matching | Broader language; not centered on interpreter↔VM equivalence evidence | Highlights design tradeoffs when match is one feature among many |
| Haskell | Expression-first bias | Looping often via recursion; different runtime model | Helps motivate `cycle` as explicit state evolution |
| Erlang | Tagged-value control patterns | Concurrent fault-tolerant runtime; different determinism assumptions | Reinforces SuayLang’s deterministic, single-process scope |
| WebAssembly | Bytecode VM model | Bytecode is the spec target; validation is standardization-based | Contrasts “bytecode-as-spec” vs “bytecode-as-backend validated vs interpreter” |
| QuickCheck | Seeded randomized testing | Typically properties with generators and shrinking | Supports the methodological choice of deterministic generation for reproducibility |
| Csmith | Random program generation for compilers | Targets C compilers; different semantics and undefined behavior issues | Shows that generation+differential oracles can find backend divergences |
| Crafting Interpreters | Interpreter+VM educational pipeline | Not centered on equivalence measurement as a research claim | Motivates making the evaluation harness part of the artifact |
