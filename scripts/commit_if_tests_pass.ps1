param(
    [Parameter(Mandatory = $true)]
    [string]$Message,

    [string]$Remote = "origin",
    [string]$Branch = ""
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

$repoRoot = (Resolve-Path ".").Path
Write-Host "Repository: $repoRoot"

$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit."
    exit 0
}

Write-Host "Running full validation before commit..."
Invoke-Checked { .\scripts\test_all.ps1 }

Write-Host "Staging changes..."
Invoke-Checked { git add . }

Write-Host "Creating commit..."
Invoke-Checked { git commit -m $Message }

if ([string]::IsNullOrWhiteSpace($Branch)) {
    $Branch = git branch --show-current
}

if ([string]::IsNullOrWhiteSpace($Branch)) {
    throw "Could not determine current branch. Pass -Branch explicitly."
}

Write-Host "Pushing to $Remote/$Branch..."
Invoke-Checked { git push $Remote $Branch }

Write-Host "Commit and push complete."

