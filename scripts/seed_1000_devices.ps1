param(
    [int]$Port = 8080,
    [int]$Count = 1000
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$baseUrl = "http://127.0.0.1:$Port"

Write-Host "Seeding $Count generated test devices into $baseUrl..."
python .\scripts\seed_bulk_devices.py --base-url $baseUrl --count $Count
Write-Host "Done. Login to the dashboard and click Refresh."

