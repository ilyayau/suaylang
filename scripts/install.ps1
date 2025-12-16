Param(
  [string]$Python = "",
  [switch]$Dev
)

$ErrorActionPreference = "Stop"

# One-shot local install for a fresh clone.
# Creates .venv, installs suaylang, runs health check, prints next steps.

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot ".."))
Set-Location $RepoRoot

function Resolve-Python {
  param([string]$Py)
  if ($Py -ne "") { return $Py }
  if (Get-Command py -ErrorAction SilentlyContinue) { return "py -3" }
  if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
  throw "python not found (need Python 3.10+)"
}

$PyCmd = Resolve-Python -Py $Python

# Check version
& $PyCmd -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" | Out-Null
if ($LASTEXITCODE -ne 0) {
  throw "Python 3.10+ required"
}

if (-Not (Test-Path ".venv")) {
  & $PyCmd -m venv .venv | Out-Null
}

$VenvPython = Join-Path ".venv" "Scripts\python.exe"

& $VenvPython -m pip install -U pip | Out-Null
if ($Dev) {
  & $VenvPython -m pip install -e ".[dev]" | Out-Null
} else {
  & $VenvPython -m pip install -e . | Out-Null
}

Write-Host "== suay doctor =="
& $VenvPython -m suaylang doctor

Write-Host ""
Write-Host "Next steps:"
Write-Host "  suay run examples/hello.suay"
Write-Host "  suay new my-project"
Write-Host "  cd my-project"
Write-Host "  suay run src/main.suay"
Write-Host "  See docs/REFERENCE_SHEET.md"
