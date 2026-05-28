Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Setting up local development environment..."

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r .\backend\requirements.txt

Write-Host "Environment setup complete."

