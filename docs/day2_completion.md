# Day 2 Completion

## Completed Scope

The device simulator now has enough behavior to represent a real embedded reliability process at a portfolio-project level.

Implemented:

- Config-driven device identity and site identity.
- Configurable telemetry interval.
- Bounded periodic telemetry generation.
- Structured telemetry JSON output.
- Health evaluation for healthy, degraded, and critical states.
- Reason-code classification for CPU, memory, and thermal pressure.
- Diagnostics JSON output when the device is degraded or critical.
- Recovery recommendation output for degraded and critical health.
- Scenario configs for healthy, degraded, and critical demos.
- C++ tests covering config loading, telemetry output, diagnostics, and recovery recommendations.

## Demo Commands

Build and test:

```powershell
.\scripts\test_all.ps1
```

Healthy:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_healthy.json
```

Degraded:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_degraded.json
```

Critical:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_critical.json
```

## Interview Framing

Day 2 shows the device-side reliability loop before adding network transport. This is deliberate: device health evaluation, diagnostics, and recovery recommendations are testable without depending on MQTT availability.

The next engineering step is Week 3: publish these telemetry and diagnostics payloads to MQTT topics.

