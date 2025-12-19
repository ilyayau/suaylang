# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-19

### Added

- `suay --version` for quick install verification.
- `suay run .` support (runs `src/main.suay` in a project directory).
- `suay new --template` with `starter` and `2d` templates.

## [0.1.0] - 2025-12-15

### Added

- SuayLang interpreter (reference semantics) with span-based diagnostics.
- Minimal bytecode compiler + stack VM for a supported subset.
- CLI (`suay`) with `run`, `check`, `ast`, and `doctor` commands.
- Minimal standard library builtins and example programs.
- Tests (unit + stress) including a “no Python tracebacks” UX constraint.
- VS Code extension (syntax highlighting + minimal LSP client/server).

[0.2.0]: https://github.com/ilyayau/suaylang/releases/tag/v0.2.0
[0.1.0]: https://github.com/ilyayau/suaylang/releases/tag/v0.1.0
