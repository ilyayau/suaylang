# Semantic scope (SuayLang v0.1)

This document freezes what is considered baseline semantics for research evaluation.
It is intentionally conservative and distinguishes language semantics from tooling and implementation artifacts.

## Baseline semantics (authoritative)

**Baseline semantics for v0.1 are defined by the reference interpreter behavior**, constrained by the v0.1 language contract.

Primary sources:
- docs/LANGUAGE_CONTRACT_v0.1.md (normative for v0.1)
- docs/GRAMMAR.md (syntax and precedence)

When a discrepancy exists between documents and implementation, the interpreter is treated as the baseline for evaluation, and discrepancies should be documented as limitations.

## Stable vs. unstable within v0.1

### Stable in v0.1 patch releases (0.1.x)

- Surface syntax and parsing rules as described in docs/GRAMMAR.md.
- Meaning of core constructs:
  - `dispatch` (first-match wins)
  - `cycle` (explicit state machine with `↩` continue and `↯` finish)
  - binding (`←`) and mutation (`⇐`)
  - lexical scoping and closure behavior
- Existence and basic behavior of the documented builtins set (docs/STDLIB.md).
- Error *categories* (lex/syntax/runtime) and span-based diagnostics.

### Unstable / allowed to change in v0.1.x (non-semantic)

- Exact wording of error messages.
- Stack trace formatting and frame labels.
- Bytecode format and instruction names (implementation detail).
- Performance characteristics.
- IDE/tooling behavior (LSP, editor features).

## VM scope for evaluation

The VM is treated as an implementation artifact.

Equivalence claims are limited to a **documented, VM-supported subset**, defined operationally as:
- programs that parse under v0.1, and
- programs whose AST nodes are supported by the compiler/VM.

Out-of-scope unless explicitly stated:
- module loading via `link` (interpreter-only in current v0.1)
- constructs not implemented by the compiler
- interactive I/O (`hear`) unless test harness supplies deterministic input

## What evaluation results can and cannot claim

Permitted claims (if supported by evidence):
- interpreter↔VM observational equivalence on the supported subset
- relative interpreter vs VM timing on specific micro-programs
- rubric-based descriptive differences in control-flow expression style vs baseline language

Not permitted without additional evidence:
- broad comprehension/readability claims across populations
- cross-language performance claims
- claims about equivalence outside the documented subset
