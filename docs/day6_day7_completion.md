# Day 6 And Day 7 Completion

## Day 6: Interactive Dashboard

Implemented:

- Static interactive web dashboard.
- Fleet health summary.
- Device telemetry table.
- Diagnostics panel.
- Recovery history panel.
- Backend health refresh button.
- Mock fleet reload button.
- Tests that verify dashboard web assets and interactive controls.

Run:

```powershell
Start-Process .\dashboard\web\index.html
```

## Day 7: AI Anomaly Detection

Implemented:

- Telemetry feature extraction.
- Baseline anomaly detector.
- Inference service.
- Backend anomaly scoring endpoint.
- Tests for normal, degraded, and critical scoring.

Backend endpoint:

```text
POST /api/anomaly/score
```

Example:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/anomaly/score" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"device_id":"ring-sim-critical","cpu_percent":97,"memory_percent":88,"temperature_celsius":72,"uptime_seconds":240}'
```

Expected:

```text
severity   : critical
is_anomaly : True
```

## Verification

```powershell
.\scripts\test_all.ps1
```

Expected:

```text
All tests passed.
```

