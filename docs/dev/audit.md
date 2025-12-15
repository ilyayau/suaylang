# Repo audit (Phase 0 baseline)

Date: 2025-12-16  
Repo: https://github.com/ilyayau/suaylang

## Quick baseline (clean environment)

Commands used for a clean baseline on Linux:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"

python -m ruff check .
python -m ruff format --check .
pytest -q
python scripts/smoke.py
python -m build
```

Observed baseline status at audit time:
- Lint: pass
- Format: pass
- Tests: 66 passed
- Smoke: `smoke:ok`
- Build: sdist + wheel succeed

## What’s in the repo (modules)

Core implementation (Python):
- Lexer / tokens: [suaylang/lexer.py](../../suaylang/lexer.py), [suaylang/tokens.py](../../suaylang/tokens.py)
- Parser / AST: [suaylang/parser.py](../../suaylang/parser.py), [suaylang/ast.py](../../suaylang/ast.py)
- Interpreter: [suaylang/interpreter.py](../../suaylang/interpreter.py)
- Bytecode compiler + VM: [suaylang/compiler.py](../../suaylang/compiler.py), [suaylang/bytecode.py](../../suaylang/bytecode.py), [suaylang/vm.py](../../suaylang/vm.py)
- Runtime + errors: [suaylang/runtime.py](../../suaylang/runtime.py), [suaylang/errors.py](../../suaylang/errors.py)
- CLI entry points: [suaylang/cli.py](../../suaylang/cli.py), [suaylang/__main__.py](../../suaylang/__main__.py)

Tooling:
- Minimal LSP: [suaylang/lsp_server.py](../../suaylang/lsp_server.py)
- VS Code extension: [vscode-extension/](../../vscode-extension/)

Tests:
- pytest suite under [tests/](../../tests/)
- Includes CLI UX tests enforcing **no Python tracebacks** in user-facing output.

Docs and examples:
- Docs in [docs/](../)
- Examples in [examples/](../../examples/)
- Smoke script runs representative examples: [scripts/smoke.py](../../scripts/smoke.py)

## Current CI / packaging state

- CI exists but is Linux-only at audit time: [.github/workflows/ci.yml](../../.github/workflows/ci.yml)
- Packaging is via `pyproject.toml` with setuptools backend: [pyproject.toml](../../pyproject.toml)
- Dev extras currently include ruff/pytest/build/hypothesis.

## Gaps vs “production-grade OSS” success metrics

High-priority gaps:
1. CI OS matrix: add Windows + macOS.
2. Coverage in CI with an enforced threshold (target >= 85%).
3. Pre-commit hooks for contributor ergonomics.
4. Static typing baseline (pyright or mypy) enforced in CI.
5. Packaging validation hardening: `twine check dist/*` in CI.

Medium-priority gaps:
- ASCII aliases for Unicode-heavy syntax (accessibility / non-Unicode keyboard support).
- Golden tests layout for stable stdout/stderr snapshots (some coverage exists via smoke + CLI tests).
- Repo maintainer signals: issue/PR templates, roadmap milestones.

## Tokenization notes (current)

The language’s surface syntax uses many Unicode tokens (e.g., `←`, `⇐`, `⌁`, `⟪`, `⟫`, `↩`, `↯`, `▷`, `⟲`, `⊤`, `⊥`).

Current implementation status:
- Lexer recognizes the Unicode symbols for the token set defined in [suaylang/lexer.py](../../suaylang/lexer.py).
- ASCII-only alternatives are not yet guaranteed across the whole surface syntax.

Planned audit follow-up:
- Add a documented Unicode→ASCII token table.
- Implement lexer aliases in a non-ambiguous way.
- Add tests ensuring Unicode and ASCII spellings produce identical tokens / AST and identical behavior.
