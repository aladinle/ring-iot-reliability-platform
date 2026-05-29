param(
    [int]$Port = 8080
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$baseUrl = "http://127.0.0.1:$Port"

Write-Host "Seeding demo telemetry, diagnostics, recovery, and anomaly events at $baseUrl"

Invoke-RestMethod `
    -Uri "$baseUrl/api/telemetry/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-healthy","cpu_percent":24,"memory_percent":48,"temperature_celsius":39.5,"uptime_seconds":120}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/telemetry/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-degraded","cpu_percent":84,"memory_percent":61,"temperature_celsius":52,"uptime_seconds":180}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/telemetry/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-critical","cpu_percent":97,"memory_percent":88,"temperature_celsius":72,"uptime_seconds":240}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/diagnostics/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-degraded","health_state":"degraded","severity":"warning","reason_code":"high_cpu","recommended_action":"reset_network"}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/diagnostics/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-critical","health_state":"critical","severity":"critical","reason_code":"memory_pressure","recommended_action":"restart_service"}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/recovery/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-degraded","action":"reset_network","result":"started","attempt":1,"reason_code":"high_cpu"}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/recovery/ingest" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-critical","action":"restart_service","result":"started","attempt":1,"reason_code":"memory_pressure"}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/anomaly/score" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-degraded","cpu_percent":84,"memory_percent":61,"temperature_celsius":52,"uptime_seconds":180}' | Out-Null

Invoke-RestMethod `
    -Uri "$baseUrl/api/anomaly/score" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"device_id":"ring-sim-critical","cpu_percent":97,"memory_percent":88,"temperature_celsius":72,"uptime_seconds":240}' | Out-Null

Write-Host "Demo data seeded. Login as operator/operator123, then click Refresh in the dashboard."
