$ErrorActionPreference = 'Stop'
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -U pip
pip install -e .
python -m pytest -q
if ($args[0] -eq '--full') {
  make reproduce-all
} else {
  make research
}
Write-Output 'REPRODUCED OK'
