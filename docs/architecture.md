# Architecture

## High-Level Architecture

The platform is divided into four primary engineering domains:

- Device simulator: C++17 embedded Linux-style process responsible for local telemetry, health checks, watchdog behavior, and recovery orchestration.
- Messaging layer: MQTT broker responsible for low-latency, topic-oriented device communication.
- Backend platform: FastAPI service responsible for telemetry ingestion, diagnostics normalization, alert coordination, and dashboard APIs.
- Intelligence and visibility: AI anomaly detection service and Qt dashboard for reliability analysis and operator workflows.

```text
+----------------------+       +-------------------+
| Device Simulator     |       | Device Config     |
| C++17 / Linux        |<----->| thresholds, IDs   |
+----------+-----------+       +-------------------+
           |
           | MQTT publish
           v
+----------------------+
| MQTT Broker          |
| telemetry topics     |
+----------+-----------+
           |
           | MQTT subscribe
           v
+----------------------+       +--------------------+
| Backend Services     |------>| Alert Processing   |
| FastAPI              |       | severity, routing  |
+----------+-----------+       +--------------------+
           |
           | REST APIs
           v
+----------------------+       +--------------------+
| Qt Dashboard         |<----->| AI Engine          |
| fleet monitoring     |       | anomaly detection  |
+----------------------+       +--------------------+
```

## Device, Backend, And Dashboard Communication Flow

```text
Device boot
  |
  v
Load local config
  |
  v
Start telemetry, health, and watchdog loops
  |
  v
Publish heartbeat and telemetry to MQTT
  |
  v
Backend receives and normalizes telemetry
  |
  v
Diagnostics service evaluates reliability state
  |
  +--> Alert service records operator-visible issue
  |
  +--> AI engine receives feature vector for anomaly scoring
  |
  v
Dashboard displays fleet state, device state, and recovery history
```

## MQTT Workflow

MQTT is used for device-originated telemetry because it fits constrained and intermittently connected systems. The intended topic design keeps message categories separate and supports future fleet scaling.

Suggested topics:

```text
devices/{device_id}/telemetry
devices/{device_id}/heartbeat
devices/{device_id}/diagnostics
devices/{device_id}/recovery
fleet/{site_id}/alerts
```

Initial MQTT design goals:

- Use device-specific topics for routing and observability.
- Keep telemetry payloads compact and schema-driven.
- Separate heartbeat messages from detailed metrics.
- Use QoS levels intentionally based on message criticality.
- Add retained status only for last-known device state, not high-volume telemetry.

## Telemetry Lifecycle

```text
Collect -> Validate -> Normalize -> Publish -> Ingest -> Store -> Analyze -> Display
```

1. Collect: Device simulator samples CPU, memory, temperature, network, and uptime metrics.
2. Validate: TelemetryManager checks value ranges and required fields.
3. Normalize: Payloads are converted into a stable schema.
4. Publish: MQTT client sends metrics to the broker.
5. Ingest: Backend receives telemetry through MQTT subscriber or HTTP endpoint.
6. Store: Future implementation persists telemetry and derived health state.
7. Analyze: Diagnostics and AI systems evaluate reliability signals.
8. Display: Dashboard surfaces health, alerts, and recovery status.

## Diagnostics Engine Design

The diagnostics engine should be rule-based first, with AI anomaly detection added as a supporting signal. This keeps early reliability behavior explainable.

Core diagnostic responsibilities:

- Evaluate telemetry thresholds.
- Detect missed heartbeat windows.
- Track repeated transient failures.
- Classify severity and reason codes.
- Emit alert-ready diagnostic events.
- Recommend recovery actions without directly executing them.

```text
Telemetry Snapshot
       |
       v
Diagnostics Rules
       |
       +--> Health state: healthy / degraded / critical
       |
       +--> Reason code: high_cpu, memory_pressure, heartbeat_timeout
       |
       v
Recovery Recommendation
```

## Self-Healing Workflow

Self-healing must be bounded, auditable, and conservative.

```text
Fault detected
  |
  v
Classify severity and root signal
  |
  v
Check recovery policy and attempt history
  |
  v
Execute simulated recovery action
  |
  v
Observe post-recovery health window
  |
  +--> recovered: record success
  |
  +--> still degraded: escalate alert
```

Candidate recovery actions:

- Restart simulated application service.
- Reset network connection.
- Enter degraded safe mode.
- Reduce telemetry frequency under resource pressure.
- Escalate to operator when automated attempts are exhausted.

## Scalability Discussion

The architecture is intended to scale from one simulated device to a fleet:

- MQTT topics naturally partition device traffic by device ID and site ID.
- Backend services can separate ingestion, diagnostics, alerting, and dashboard APIs.
- Telemetry storage can evolve from local development storage to time-series infrastructure.
- AI inference can run asynchronously to avoid blocking ingestion.
- Dashboard APIs can use cached fleet health summaries for operator responsiveness.

Future production considerations:

- Backpressure handling for telemetry spikes.
- Device identity and authentication.
- Broker clustering and durable subscriptions.
- Schema versioning.
- Observability for backend service health.
- Deployment topology across edge gateways and cloud services.

## Edge Vs Cloud Processing

Edge processing is best for low-latency safety decisions, watchdog behavior, and local recovery. Cloud processing is better for fleet-wide trend analysis, historical anomaly detection, dashboards, and cross-device correlation.

This project separates those concerns:

- Device edge logic: immediate health checks, watchdog timers, local recovery decisions.
- Backend/cloud logic: aggregation, alert history, fleet visibility, long-range diagnostics.
- AI logic: anomaly scoring based on historical or fleet-level context.

The result is a reliability model where devices can protect themselves locally while the backend provides broader operational intelligence.

