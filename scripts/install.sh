#!/usr/bin/env bash
set -euo pipefail

# One-shot local install for a fresh clone.
# Creates .venv, installs suaylang, runs health check, prints next steps.

dev=0
if [[ "${1:-}" == "--dev" ]]; then
  dev=1
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

py="${PYTHON:-}"
if [[ -z "$py" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    py=python3
  elif command -v python >/dev/null 2>&1; then
    py=python
  else
    echo "error: python not found (need Python 3.10+)" >&2
    exit 1
  fi
fi

"$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' \
  || { echo "error: Python 3.10+ required" >&2; exit 1; }

if [[ ! -d .venv ]]; then
  "$py" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install -U pip >/dev/null
if [[ "$dev" -eq 1 ]]; then
  python -m pip install -e ".[dev]"
else
  python -m pip install -e .
fi

echo "== suay doctor =="
suay doctor

echo
cat <<'TXT'
Next steps:

  # Run a known-good example
  suay run examples/hello.suay

  # Start a new project
  suay new my-project
  cd my-project
  suay run src/main.suay

  # Reference sheet
  See docs/REFERENCE_SHEET.md

If you installed without dev dependencies and want to run tests later:
  python -m pip install -e ".[dev]"
TXT
