# Final Release Checklist

## Verification

```powershell
.\scripts\test_all.ps1
.\scripts\verify_mqtt.ps1
```

Expected:

```text
All tests passed.
MQTT verification passed.
```

## Demo

```powershell
.\scripts\run_full_demo.ps1
```

The script prints the commands to run in separate PowerShell windows.

## Portfolio Talking Points

- C++17 simulator models embedded Linux device behavior.
- MQTT carries telemetry, diagnostics, and recovery events.
- FastAPI backend provides ingestion, auth, dashboard state, anomaly scoring, and history.
- SQLite persists reliability event history.
- Repository boundary allows later MySQL migration.
- Dashboard supports login, live refresh, history, diagnostics, recovery, and anomaly panels.

## Known Limitations

- Auth is demo-only and not production-grade.
- SQLite is local persistence, not a multi-user production database.
- MQTT bridge is dependency-free and local-demo oriented.
- Dashboard is a static web UI, with Qt shell preserved for a future native app.

