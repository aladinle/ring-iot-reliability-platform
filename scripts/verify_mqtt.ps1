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

Write-Host "Starting MQTT broker..."
Invoke-Checked { docker compose -f .\docker\docker-compose.yml up -d mqtt-broker }

Write-Host "Building simulator..."
Invoke-Checked { .\scripts\build_cpp.ps1 }

Write-Host "Starting MQTT subscriber for devices/#..."
$repoRoot = (Resolve-Path ".").Path
$subscriber = Start-Job -ScriptBlock {
    param($WorkingDirectory)
    Set-Location $WorkingDirectory
    docker compose -f .\docker\docker-compose.yml exec -T mqtt-broker `
        mosquitto_sub -t "devices/#" -C 3 -W 10 -v
} -ArgumentList $repoRoot

Start-Sleep -Seconds 2

Write-Host "Publishing degraded simulator scenario over MQTT..."
Invoke-Checked {
    .\device_simulator\build\Debug\device_simulator.exe `
        .\device_simulator\config\scenario_degraded.json `
        --mqtt
}

$messages = Receive-Job -Job $subscriber -Wait
Remove-Job -Job $subscriber

Write-Host "Received MQTT messages:"
$messages | ForEach-Object { Write-Host $_ }

if (-not ($messages -match "devices/ring-sim-degraded/telemetry")) {
    throw "Telemetry MQTT message was not observed."
}

if (-not ($messages -match "devices/ring-sim-degraded/diagnostics")) {
    throw "Diagnostics MQTT message was not observed."
}

if (-not ($messages -match "devices/ring-sim-degraded/recovery")) {
    throw "Recovery MQTT message was not observed."
}

Write-Host "MQTT verification passed."
