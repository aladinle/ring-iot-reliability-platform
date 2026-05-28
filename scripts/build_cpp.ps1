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

$buildDir = "device_simulator\build"

if (-not (Test-Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir | Out-Null
}

Invoke-Checked { cmake -S .\device_simulator -B $buildDir }
Invoke-Checked { cmake --build $buildDir }
Invoke-Checked { ctest --test-dir $buildDir -C Debug --output-on-failure }
