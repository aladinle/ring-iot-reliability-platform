# Device Simulator

The device simulator models the embedded Linux side of the reliability platform. It will eventually simulate a connected device process with telemetry collection, health monitoring, watchdog supervision, MQTT communication, and recovery orchestration.

This module intentionally starts with class boundaries and build structure only.

## Planned Responsibilities

- Manage device lifecycle state.
- Generate telemetry snapshots.
- Monitor health thresholds.
- Detect watchdog timeouts.
- Coordinate bounded recovery actions.
- Publish telemetry and diagnostics events through MQTT.

## Build

```powershell
.\scripts\build_cpp.ps1
```

