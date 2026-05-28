# Day 3 MQTT Communication

Day 3 connects the device simulator to the local MQTT broker. The simulator can still print telemetry and diagnostics to stdout, but when `--mqtt` is passed it also publishes payloads to MQTT topics.

## Implemented Scope

- MQTT topic builder for device telemetry, diagnostics, heartbeat, and recovery topics.
- Minimal C++ MQTT 3.1.1 QoS 0 publisher for local broker publishing.
- Optional simulator `--mqtt` mode.
- MQTT config parsing from device scenario files.
- Automated MQTT smoke verification script.
- C++ tests for MQTT topic construction and config parsing.

## Topic Format

```text
devices/{device_id}/telemetry
devices/{device_id}/diagnostics
devices/{device_id}/heartbeat
devices/{device_id}/recovery
```

## Start Broker

```powershell
.\scripts\run_mqtt.ps1
```

## Run Simulator With MQTT

In another PowerShell window:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_degraded.json --mqtt
```

## Automated MQTT Smoke Test

```powershell
.\scripts\verify_mqtt.ps1
```

The script:

- Starts Mosquitto through Docker Compose.
- Builds the C++ simulator.
- Subscribes to `devices/#`.
- Runs the degraded simulator scenario with `--mqtt`.
- Fails if telemetry or diagnostics messages are not observed.

## Manual Subscriber

```powershell
docker compose -f .\docker\docker-compose.yml exec -T mqtt-broker mosquitto_sub -t "devices/#" -v
```

Then publish with:

```powershell
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\scenario_critical.json --mqtt
```

## Notes

The publisher is intentionally small and supports local QoS 0 publishing. Later production hardening should add reconnect backoff, authentication, TLS, QoS policy, and a tested third-party MQTT client if project scope requires it.

