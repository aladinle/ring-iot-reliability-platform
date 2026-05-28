# MQTT Contract

This document defines the first device messaging contract for the platform. It is intentionally small and stable so implementation can begin without overbuilding the broker integration.

## Topic Naming

```text
devices/{device_id}/telemetry
devices/{device_id}/heartbeat
devices/{device_id}/diagnostics
devices/{device_id}/recovery
fleet/{site_id}/alerts
```

## Telemetry Topic

Topic:

```text
devices/{device_id}/telemetry
```

Payload:

```json
{
  "schema_version": "1.0",
  "device_id": "ring-sim-001",
  "site_id": "lab-001",
  "observed_at": "2026-05-28T17:00:00Z",
  "metrics": {
    "cpu_percent": 42.0,
    "memory_percent": 55.0,
    "temperature_celsius": 38.5,
    "uptime_seconds": 120
  }
}
```

## Heartbeat Topic

Topic:

```text
devices/{device_id}/heartbeat
```

Payload:

```json
{
  "schema_version": "1.0",
  "device_id": "ring-sim-001",
  "state": "healthy",
  "sequence": 12,
  "observed_at": "2026-05-28T17:00:00Z"
}
```

## Diagnostics Topic

Topic:

```text
devices/{device_id}/diagnostics
```

Payload:

```json
{
  "schema_version": "1.0",
  "device_id": "ring-sim-001",
  "health_state": "degraded",
  "severity": "warning",
  "reason_code": "memory_pressure",
  "recommended_action": "reset_network",
  "observed_at": "2026-05-28T17:00:00Z"
}
```

## Recovery Topic

Topic:

```text
devices/{device_id}/recovery
```

Payload:

```json
{
  "schema_version": "1.0",
  "device_id": "ring-sim-001",
  "action": "restart_service",
  "result": "started",
  "attempt": 1,
  "reason_code": "watchdog_timeout",
  "observed_at": "2026-05-28T17:00:00Z"
}
```

## Initial QoS Guidance

- Telemetry: QoS 0 for high-volume metrics during local development.
- Heartbeat: QoS 1 when missed messages affect device state.
- Diagnostics: QoS 1 because alerts should not be silently dropped.
- Recovery: QoS 1 because recovery audit events matter.

## Implementation Notes

- Payloads should include `schema_version` from the beginning.
- Device IDs should be stable and unique.
- Backend ingestion should reject unknown schema versions once validation is implemented.
- Recovery events should be append-only for auditability.

