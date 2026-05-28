param(
    [int]$Port = 8080
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    Write-Host "Virtual environment not found. Running setup first..."
    .\scripts\setup_env.ps1
}

Write-Host "Starting backend at http://127.0.0.1:$Port"
& .\.venv\Scripts\uvicorn.exe backend.main:app --reload --host 127.0.0.1 --port $Port
