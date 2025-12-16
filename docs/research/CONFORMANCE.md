# Interpreter vs VM conformance (SuayLang v0.1)

This document defines a *conservative* conformance claim and the evidence produced by the repository.

## Why conformance matters here

SuayLang intentionally has:
- a reference interpreter (semantic authority for v0.1), and
- a bytecode compiler + VM (engineering exploration; implementation artifact).

A research-grade evaluation requires evidence that the VM does not silently diverge from the interpreter on the supported subset.

## Observational equivalence (definition)

For a program $P$ in the **supported conformance subset**:

Two executions are observationally equivalent if they agree on:
1) **Termination kind**: success vs user-facing error (lex/syntax/runtime).
2) **Stdout**: exact text printed by the program (normalized to `\n` newlines).
3) **Result value** (on success): structural equality of returned runtime values *excluding* opaque function objects.
4) **Error category + location** (on error):
   - lexical/syntax errors: same error category; span location is reported by the lexer/parser
   - runtime errors: both raise a runtime error; compare span start line/column when available

Non-goals (explicit):
- Exact wording of error messages is not required in the relaxed equivalence mode (v0.1 contract allows wording changes).
- Stack trace frames are not required to match.

## Supported conformance subset

Conformance is claimed only for programs that:
- parse under the v0.1 grammar, and
- are supported by the current compiler/VM (subset of AST nodes).

Examples of constructs **excluded** from the claim (treated as “not evaluated”):
- module loading via `link` (interpreter supports modules; VM does not)
- any AST node the compiler marks as NotImplemented

## Evidence in this repository

- Shared corpus: tests/corpus/conformance/*.suay
- Differential runner: scripts/conformance.py
- CI enforcement: tests/test_conformance_corpus.py
- Generative component (bounded): tests/test_conformance_fuzz.py

## How to run

```sh
python scripts/conformance.py
pytest -q -k conformance
```

## Interpreting failures

A conformance failure is treated as:
- a VM bug,
- or a mismatch in which construct is considered “supported,”
- or a test that accidentally relies on unspecified behavior.

All failures should be triaged with:
- the minimal reproducer program,
- the interpreter vs VM stdout,
- the error category and span.
