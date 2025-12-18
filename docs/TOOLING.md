# SuayLang Tooling (closed-loop, v0.1)

This document describes the `suay` CLI surface as a contract.

Canonical syntax in docs is ASCII-first. See [docs/ASCII_SYNTAX.md](ASCII_SYNTAX.md).

## Commands

### `suay doctor`

- Purpose: deterministic self-check that exercises `lex -> parse -> interpret`.
- Output: prints environment info and `OK` on success.

### `suay run <file>`

- Executes a `.suay` source file with the reference interpreter.
- Failures are reported as user-facing diagnostics with file/line/column.

### `suay run -e '<source>'`

- Executes inline source as a single program.

### `suay check <file>`

- Lex+parse only; no execution.

### `suay ast <file>`

- Prints the parsed AST (debugging convenience).

### `suay repl`

- Experimental REPL.
- REPL printing is not part of the language contract.

### `suay fmt <files...>`

- Rewrites source into canonical spelling.
- Default: ASCII output.
- Options:
  - `--check` checks without modifying files (non-zero exit if changes needed).
  - `--unicode` emits Unicode spellings instead of ASCII.

Notes:
- Current formatter is rewrite-first (it preserves whitespace/comments and only canonicalizes token spellings).

### `suay test [-- <pytest args...>]`

- Convenience wrapper around `pytest` (requires dev dependencies).
- Repo-level contract tests live under `tests/`.

### Contract helpers

- `suay ref <topic>` prints a canonical doc reference path.
- `suay explain <E-...>` prints the section for a stable error code.

## Exit codes

- `0` success
- `1` user-facing failure (lex/syntax/runtime or IO)
- `2` CLI usage error

## Roadmap (non-contract)

Future PRs (tracked in the release plan) will add:
- `suay pkg init|build|add|lock`
- `suay run <module>` (module graph entrypoints)
- `suay test` running project tests + conformance in one command
