# Baselines and analytical comparison

This project is not claiming novelty by “being a language”. The baseline comparison is about *how SuayLang packages explicit control flow + diagnostics + backend equivalence evidence*.

## 1) Comparison table (3–5 baselines)

| Baseline | Control flow (stmt vs expr) | Pattern matching centrality | Semantics explicitness | Error model | Tooling story | VM/interpreter equivalence strategy | Accessibility (ASCII-first) | Target use-case |
|---|---|---|---|---|---|---|---|---|
| **Python 3.10+** (`match`/statements) | Mostly statements; expressions exist | Medium (optional) | Informal spec + reference impl | Exceptions; tracebacks | Strong ecosystem; static tools | No built-in equivalence harness | ASCII | General-purpose scripting |
| **Rust** (`match` expr) | Many constructs expression-shaped | Medium-high | Precise RFC/spec ecosystem | `Result` + panics; spans in compiler | Excellent diagnostics | Compiler test suite; not differential vs a reference interpreter | ASCII | Systems programming |
| **OCaml** / **Haskell** | Expression-first | High | Formal-ish core semantics; mature theory | Algebraic data types; exceptions optional | Strong type-driven tooling | Not typically validated via “interpreter vs VM” differential testing | ASCII | FP + PL teaching |
| **Lua** | Statements + expressions (small core) | Low | Small reference manual | Error strings + stack traces | Embeddable; simple tooling | Usually single implementation; no continuous equivalence evidence | ASCII | Embedded scripting |
| **Wasm / bytecode VMs** (execution model) | Stack machine; structured control | N/A | Formal spec (often) | Traps; structured validation errors | Tooling around validation/disassembly | Conformance suites exist; differential testing common | ASCII-ish | Portable execution target |

## 2) Related work (analytical, 8–12 bullets)

- **QuickCheck (Claessen & Hughes)**: similar goal (generate diverse tests), differs because SuayLang targets *cross-backend equivalence* and stores minimized regressions as part of the artifact.
- **Differential testing (McKeeman)**: SuayLang directly applies the technique: interpreter is the reference, VM is the system-under-test.
- **C compiler differential testing (Yang et al.)**: similar methodology at larger scale; SuayLang is smaller but aims for the same reviewer-friendly property: failures are reproducible via seeds.
- **Operational semantics (Plotkin/Kahn)**: SuayLang is not presenting a formal semantics here; instead it encodes an operational contract as executable observation equivalence.
- **Rust diagnostics culture**: SuayLang borrows the idea that diagnostics are part of the language contract; it differs by testing diagnostic *span stability* across two backends.
- **Crafting Interpreters-style systems**: similar educational implementation style; SuayLang differs by making equivalence and evidence artifacts a core deliverable.
- **Wasm conformance suites**: similar in that “execution model correctness” is tested continuously; SuayLang differs by focusing on language-level constructs (dispatch/cycle) rather than low-level validation.
- **Expression-oriented control flow** (ML-family): SuayLang aligns with expression-first forms; it differs by designing an explicit state-machine loop (`cycle`) as a surface construct rather than relying on recursion.
- **Tooling-first language design**: SuayLang treats formatter + ASCII aliases + error codes as part of the research artifact rather than post-hoc tooling.

