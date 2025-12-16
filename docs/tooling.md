# Tooling status

This document summarizes the current tooling support for SuayLang.

## CLI

Primary entrypoint:
- `suay` (installed via the `suaylang` Python package)

Key commands:
- `suay doctor` — installation/health check
- `suay run <file>` — execute a program
- `suay run -e '<code>'` — inline execution (playground)
- `suay check <file>` — lex+parse only
- `suay ast <file>` — print AST
- `suay new <project>` — create a starter project
- `suay repl` — experimental interactive mode
- `suay test` — convenience wrapper for pytest (requires dev deps)
- `suay fmt` — placeholder (planned)

## VS Code

The repository includes a VS Code extension under:
- vscode-extension/suaylang/

It provides:
- Syntax highlighting
- Minimal LSP features (from suaylang/lsp_server.py):
  - Diagnostics (lexer/parser)
  - Hover (builtins + best-effort function info)
  - Go-to-definition (best-effort for bindings)
  - Document symbols

Status notes:
- The LSP server is intentionally small and conservative.
- It does not attempt full semantic analysis or type checking.

## Research tooling

- Conformance runner:
  - tools/conformance/run.py
  - tests/corpus/conformance/ (shared corpus)

- Benchmarks:
  - scripts/bench_micro.py
  - benchmarks/ (programs)
