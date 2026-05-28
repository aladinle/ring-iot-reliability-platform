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

