# Feature matrix (v0.1)

This table is meant to give reviewers a quick, concrete overview of:

- which features exist,
- whether the VM supports them,
- where they’re tested (unit/conformance/fuzz/golden), and
- which spec document covers the behavior.

Legend:

- **Interp**: implemented in interpreter
- **VM**: supported by compiler+VM
- **Conformance**: covered by interpreter↔VM corpus runner
- **Spec**: link to spec section

| Feature | Interp | VM | Tests (examples) | Conformance | Spec |
|---|:--:|:--:|---|:--:|---|
| Lexer/tokenization + spans | ✓ | ✓ | `tests/test_lexer.py`, `tests/test_ascii_syntax.py` | ✓ | docs/spec/errors.md |
| Parser + spans | ✓ | ✓ | `tests/test_parser.py`, `tests/test_parser_pytest.py` | ✓ | docs/spec/errors.md |
| Binding (`←` / `<-`) | ✓ | ✓ | `tests/test_interpreter.py`, `tests/test_ascii_syntax.py` | ✓ | docs/spec/control_flow.md |
| Mutation (`⇐` / `<~`) | ✓ | ✓ | `tests/test_runtime_primitives.py` | ✓ | docs/spec/control_flow.md |
| Blocks (`⟪⟫` / `{}`) | ✓ | ✓ | `tests/test_interpreter.py` | ✓ | docs/spec/control_flow.md |
| Lambda + closures (`⌁` / `\`) | ✓ | ✓ | `tests/test_interpreter.py` | ✓ | docs/spec/control_flow.md |
| Call (`·` / `.`) | ✓ | ✓ | `tests/test_interpreter.py`, `tests/test_ascii_syntax.py` | ✓ | docs/spec/control_flow.md |
| Variants (`•` / `::`) | ✓ | ✓ | `tests/test_runtime_primitives.py` | ✓ | docs/spec/control_flow.md |
| Dispatch (`▷` / `|>`) | ✓ | ✓ | `tests/test_interpreter.py`, `tests/corpus/conformance/002_dispatch.suay` | ✓ | docs/spec/control_flow.md |
| Cycle (`⟲` / `~~`) + `↩/↯` (`>>/<<`) | ✓ | ✓ | `tests/corpus/conformance/003_cycle_sum.suay` | ✓ | docs/spec/control_flow.md |
| Lists (`[ ]`) + patterns (`⋯` / `...`) | ✓ | ✓ | `tests/test_parser.py` | ✓ | docs/spec/control_flow.md |
| Maps (`⟦⟧` / `[[ ]]`, `↦` / `->`) | ✓ | ✓ | `tests/test_runtime_primitives.py`, `tests/test_ascii_syntax.py` | ✓ | docs/spec/control_flow.md |
| Modules via `link` | ✓ | ✗ | `tests/test_modules.py` | ✗ | docs/spec/errors.md |
| Golden diagnostics (stable UX) | ✓ | ✓ | `tests/test_golden_diagnostics.py` | n/a | docs/spec/errors.md |
| Parser fuzz (no crashes) | ✓ | ✓ | `tests/fuzz/test_parser_fuzz.py` | n/a | docs/testing.md |
| Differential fuzz (interp↔VM) | ✓ | ✓ | `tools/conformance/fuzz.py` | ✓ | docs/research/conformance.md |
