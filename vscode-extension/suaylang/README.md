# SuayLang VS Code Extension (local)

This folder provides **syntax highlighting** (TextMate grammar) and a **minimal LSP client** that launches the Python server in this repo.

## Features

- Syntax highlighting for `.suay`
- Bracket/quote auto-closing + line comments (`⍝`)
- LSP (from `suaylang/lsp_server.py`):
  - Diagnostics (lexer/parser errors)
  - Hover (builtins + best-effort function info)
  - Go to definition (best-effort for bindings/functions)
  - Document symbols (best-effort)

## Prereqs

- VS Code
- Node.js + npm
- Python 3 available as `python3` (or configure a different path)
- Open the **repo root** as your VS Code workspace (so `suaylang/` is importable)

## Install (from source)

1) Install Node dependencies:

```sh
cd vscode-extension/suaylang
npm install
```

Note: you can’t `node -e "require('./extension.js')"` outside VS Code because the `vscode` module is provided by VS Code at runtime.

2) Install the extension locally in VS Code:

- Command Palette → **Developer: Install Extension from Location...**
- Select this folder: `vscode-extension/suaylang`

(Alternatively: open this folder in VS Code and press **F5** to run an Extension Development Host.)

## Configure

If Python isn’t available as `python3`, set:

- Settings → `suay.server.pythonPath`

The extension launches the server with:

- `python -m suaylang.lsp_server`

## Quick test

- Open `examples/hello.suay`
- Introduce a small syntax error → you should see diagnostics
- Hover `say` or `fold` → you should get a hover popup
- Ctrl/Cmd+click a defined name (`x ← ...`) → go-to-definition should jump
