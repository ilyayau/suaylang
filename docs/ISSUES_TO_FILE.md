# Seed issues to file (copy/paste)

This repo can’t create GitHub issues without GitHub API access.
Below are 7 ready-to-file issues aligned with the roadmap.

## 1) CI: add Windows job
- Labels: `ci`, `enhancement`
- Summary: Run CI on Windows to validate install.ps1 and path handling.
- Acceptance: GitHub Actions matrix includes `windows-latest`; `suay doctor` succeeds.

## 2) CLI: implement `suay fmt`
- Labels: `enhancement`, `tooling`
- Summary: Provide a formatter or canonicalizer for Suay source (at least whitespace/newlines).
- Acceptance: `suay fmt file.suay` rewrites deterministically; idempotent.

## 3) VM: expand compiler support for modules/link
- Labels: `vm`, `enhancement`
- Summary: Decide whether `link` should be supported by VM; if not, document hard exclusion.
- Acceptance: Feature matrix updated; conformance scope updated.

## 4) Docs: add “ASCII-only tutorial path”
- Labels: `docs`, `accessibility`
- Summary: Provide a tutorial that uses only ASCII aliases.
- Acceptance: All code blocks are ASCII-only; verified by running.

## 5) Golden diagnostics: add more common mistakes
- Labels: `testing`, `bug`
- Summary: Add snapshots for common parse errors (missing arm arrow, invalid cycle mode, etc.).
- Acceptance: New `tests/golden/cases/*.suay` with stable `*.txt` outputs.

## 6) Benchmarks: add JSON/Markdown export
- Labels: `bench`, `enhancement`
- Summary: Make `scripts/bench_micro.py` optionally emit JSON or a markdown table.
- Acceptance: `--json` output documented and stable.

## 7) LSP: add diagnostics for ASCII aliases
- Labels: `lsp`, `tooling`
- Summary: Ensure LSP diagnostics/spans remain correct with ASCII alias tokens.
- Acceptance: VS Code shows correct underlines for ASCII source.
