# Dashboard

Qt-based monitoring UI placeholder for fleet health, device detail, alerts, diagnostics, and recovery history.

## Suggested Architecture

```text
dashboard/
├── ui/
│   ├── main_window/
│   ├── fleet_overview/
│   ├── device_detail/
│   └── alerts/
├── services/
│   ├── api_client/
│   └── telemetry_stream/
├── models/
│   ├── device_status/
│   └── alert_state/
└── resources/
```

## Planned Views

- Fleet overview with health state rollups.
- Device detail with latest telemetry and diagnostics.
- Alert queue with severity and acknowledgement state.
- Recovery history timeline.
- Settings for backend endpoint and refresh interval.

The dashboard should behave like an operator tool: dense, readable, and optimized for repeated monitoring workflows.

## Day 6 Implementation

Day 6 adds dashboard data contracts and a backend API client that a Qt UI can consume:

- `dashboard/models/dashboard_state.py`
- `dashboard/services/api_client/client.py`
- `dashboard/ui/main_window/MainWindow.qml`
- `dashboard/resources/fleet_snapshot.example.json`
- `dashboard/web/index.html`

The QML file is a UI shell. The Python data layer is tested in CI so dashboard-facing behavior has executable coverage without requiring Qt to be installed on every build runner.

## Interactive Web Dashboard

Open the static dashboard in a browser:

```powershell
Start-Process .\dashboard\web\index.html
```

The web dashboard provides:

- Fleet health summary.
- Device telemetry table.
- Diagnostics list.
- Recovery history list.
- Anomaly scores.
- Backend health refresh button.
- Mock fleet reload button.

When the backend is running at `http://127.0.0.1:8080`, the Refresh button also loads `GET /api/dashboard/snapshot`.
