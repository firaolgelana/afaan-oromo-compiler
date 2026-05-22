# One-time setup after cloning the repo (Windows PowerShell).
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

function Find-Python {
    if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
    if (Get-Command py -ErrorAction SilentlyContinue) { return "py -3" }
    return $null
}

$python = Find-Python
if (-not $python) {
    Write-Error "Python not found. Install Python 3.10+ from https://www.python.org/ and enable 'Add to PATH'."
    exit 1
}

Write-Host "==> Installing Afaan Oromoo transpiler (editable)..."
Invoke-Expression "$python -m pip install -e ."

Write-Host ""
Write-Host "Milkaa'ina! Run .ao programs with:"
Write-Host "  aoc test.ao"
Write-Host "  ao test.ao --run"
Write-Host "  python run.py test.ao"
Write-Host ""
Write-Host "If 'aoc' is not recognized, close and reopen the terminal, or run:"
Write-Host "  python -m pip install -e ."
Write-Host ""
Write-Host "Cursor / VS Code syntax highlighting (optional):"
Write-Host "  Extensions -> Install from Folder -> $RepoRoot\vscode-oromolang"
