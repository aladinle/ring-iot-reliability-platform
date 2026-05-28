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

## Run

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\device_config.example.json
```

Expected output includes multiple telemetry payloads shaped like the MQTT telemetry contract. The number of payloads is controlled by `sample_count` in the config file.

```json
{"schema_version":"1.0","device_id":"ring-sim-001","site_id":"lab-001","observed_at":"2026-05-28T17:00:00Z","metrics":{"cpu_percent":24,"memory_percent":48,"temperature_celsius":39.5,"uptime_seconds":0}}
```

For a faster smoke test:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\tests\fixtures\device_config.test.json
```

## Reliability Scenarios

Healthy scenario emits telemetry only:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_healthy.json
```

Degraded scenario emits telemetry and diagnostics with `high_cpu` plus a `reset_network` recommendation:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_degraded.json
```

Critical scenario emits telemetry and diagnostics with a `restart_service` recommendation:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_critical.json
```
