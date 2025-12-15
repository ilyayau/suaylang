# Architecture

This document is a reviewer-oriented overview of SuayLang’s structure and execution pipeline.

## Repository layout (core)

- `suaylang/`
  - `lexer.py`: tokenization with span/position tracking
  - `parser.py`: AST construction and syntax diagnostics
  - `ast.py`: AST node definitions (spans attached)
  - `interpreter.py`: reference evaluator + module loading
  - `compiler.py`: compiler from AST → bytecode
  - `bytecode.py`: bytecode instruction and code container
  - `vm.py`: stack VM for a supported subset
  - `errors.py`, `runtime.py`: diagnostics and runtime value model
  - `cli.py`: `suay` command implementation

## Execution pipeline

### 1) Source → tokens

- The lexer produces tokens with `(line, column)` spans.
- Lex errors are reported as diagnostics with caret context.

### 2) Tokens → AST

- The parser consumes tokens and produces a span-carrying AST.
- Parse errors are diagnostics with source context.
- Defensive handling converts deep Python recursion failures into user-facing errors.

### 3) AST → result (interpreter)

- The interpreter evaluates expressions in a lexical environment.
- Runtime errors are raised as structured `SuayRuntimeError` values with spans.
- The interpreter maintains a call stack model for error reporting.

### 4) AST → bytecode → result (VM)

- The compiler emits a small instruction set (stack machine) intended to mirror interpreter semantics.
- The VM executes bytecode with an explicit environment chain.
- VM runtime errors are raised with spans and source context.

## Error handling strategy

The project treats “reviewable failures” as a core requirement:

- Errors include file/line/column spans and caret context.
- CLI commands are expected to avoid leaking Python tracebacks for user errors.
- Tests and smoke checks enforce this constraint.
