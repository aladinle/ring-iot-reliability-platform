# AI Engine

The AI engine will provide anomaly detection for device telemetry and reliability signals.

It is intentionally isolated from the backend ingestion path so early diagnostics can stay explainable and deterministic. Future inference can run asynchronously or behind an internal API.

## Day 7 Implementation

Implemented:

- Telemetry feature extraction.
- Baseline anomaly detector.
- Inference service.
- Backend scoring endpoint at `/api/anomaly/score`.
- Tests for normal, degraded, and critical telemetry patterns.

The current detector is deterministic and rule-backed. This is intentional until realistic telemetry history exists for training and validation.

## Manual Test

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/anomaly/score" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"device_id":"ring-sim-degraded","cpu_percent":84,"memory_percent":61,"temperature_celsius":52,"uptime_seconds":180}'
```
