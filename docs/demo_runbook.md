# Demo Runbook

This runbook is the interview-friendly path for showing the project end to end.

## 1. Run Validation

```powershell
.\scripts\test_all.ps1
```

Expected:

```text
All tests passed.
```

## 2. Start Backend

```powershell
.\scripts\run_backend.ps1 -Port 8080
```

Open:

```text
http://127.0.0.1:8080/docs
```

## 3. Seed Demo Data

In another PowerShell window:

```powershell
.\scripts\seed_demo_data.ps1 -Port 8080
```

## 4. Open Dashboard

```powershell
Start-Process .\dashboard\web\index.html
```

Click `Refresh` to load backend-backed fleet state.

Demo login:

```text
operator / operator123
```

## 5. Check Persisted History

After logging in through the API:

```powershell
$login = Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/auth/login" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"username":"operator","password":"operator123"}'

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/dashboard/history" `
  -Headers @{ Authorization = "Bearer $($login.access_token)" }
```

## 6. Show MQTT Flow

```powershell
.\scripts\verify_mqtt.ps1
```

This verifies telemetry, diagnostics, and recovery messages through Mosquitto.

## Talking Points

- C++ simulates the embedded Linux device agent.
- MQTT carries device-originated telemetry and reliability events.
- FastAPI normalizes events for dashboard and AI workflows.
- The dashboard exposes fleet health, diagnostics, recovery, and anomaly state.
- AI anomaly detection supports rule-based diagnostics rather than replacing them.
