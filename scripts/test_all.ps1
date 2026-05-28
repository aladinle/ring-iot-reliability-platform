param(
    [switch]$SkipCpp
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )

    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

if (-not $SkipCpp) {
    Write-Host "Running C++ build and tests..."
    Invoke-Checked { .\scripts\build_cpp.ps1 }
}

Write-Host "Running backend tests..."
Invoke-Checked { python -m pytest tests\backend }

Write-Host "All tests passed."

