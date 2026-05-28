# Interview Talking Points

## 1. Reliability-First Architecture

The project is structured around health monitoring, diagnostics, recovery, and observability rather than feature-first application behavior. This mirrors real connected device platforms where reliability is a product requirement.

## 2. Clear Edge And Cloud Separation

Immediate watchdog and recovery behavior belongs on the device side, while aggregation, alert history, dashboards, and fleet analysis belong in backend services.

## 3. Explainable Diagnostics Before AI

Rule-based diagnostics are implemented before anomaly detection so health decisions remain auditable. AI becomes an additional signal rather than an opaque replacement for reliability rules.

## 4. Multithreaded Device Model

The simulator is designed around separate responsibilities for telemetry collection, health monitoring, watchdog supervision, and recovery coordination. This supports discussion of thread ownership, synchronization, shutdown behavior, and timing.

## 5. Why MQTT

MQTT is a strong fit for IoT systems because it is lightweight, topic-based, supports unreliable networks, and maps naturally to device telemetry, heartbeat, diagnostics, and command workflows.

## 6. Why C++17

C++17 is appropriate for embedded Linux because it provides deterministic resource control, modern standard library support, strong performance, and compatibility with production device software constraints.

## 7. Why FastAPI

FastAPI provides a clean way to build typed backend APIs quickly with Python, Pydantic models, OpenAPI documentation, and straightforward service layering for telemetry and alert workflows.

## 8. Self-Healing With Guardrails

Recovery actions should be conservative, rate-limited, observable, and reversible where possible. The project separates recovery recommendations from recovery execution so decisions can be audited.

## 9. Telemetry Lifecycle Discipline

The architecture treats telemetry as a lifecycle: collection, validation, normalization, transport, ingestion, analysis, and visualization. This creates a professional story around data quality and reliability.

## 10. AI Anomaly Detection As Fleet Intelligence

Anomaly detection is most valuable when it identifies reliability patterns that static thresholds miss, such as gradual degradation, unusual resource combinations, or fleet-wide behavior shifts.

## Architecture Decisions

- Use MQTT for device-originated communication.
- Keep backend APIs independent from device simulator internals.
- Use C++ class boundaries that map to embedded reliability concerns.
- Keep AI engine separate to avoid coupling inference behavior to telemetry ingestion.
- Add dashboard as an operator surface rather than a marketing demo.

## Reliability Engineering Decisions

- Classify degraded and critical states explicitly.
- Track recovery attempt history.
- Prefer explainable diagnostics for operational decisions.
- Treat missing telemetry as a reliability signal.
- Design alerting and recovery as separate workflows.

## Diagnostics Design

Diagnostics should evaluate snapshots, produce reason codes, assign severity, and recommend action. The engine should avoid executing recovery directly so policy remains testable.

## Threading Model Discussion

The intended simulator can use dedicated loops for telemetry, health monitoring, watchdog checks, and recovery execution. Shared state should be minimized and protected through clear ownership, immutable snapshots, or message queues.

## Technology Rationale

- MQTT: Lightweight device messaging and topic-based routing.
- C++17: Embedded Linux realism, performance, and modern language features.
- FastAPI: Typed backend surface with fast iteration.
- AI anomaly detection: Adds long-horizon and fleet-level reliability insight.

