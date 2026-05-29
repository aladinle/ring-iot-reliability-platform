# Ring IoT Reliability Platform

A professional embedded Linux and IoT reliability engineering portfolio project inspired by Ring-style smart device systems.

This repository is the Day 1 foundation for a Smart IoT Device Monitoring and Self-Healing Platform. The project is designed to showcase production-oriented thinking across embedded C++ device software, MQTT telemetry, backend services, dashboard monitoring, diagnostics, recovery automation, and AI-assisted anomaly detection.

The first milestone intentionally focuses on architecture, structure, documentation, and clean engineering workflow. Production behavior will be added incrementally.

## Project Overview

The platform simulates a fleet of smart connected devices that emit telemetry, report health status, detect degraded behavior, and trigger recovery actions. A backend service receives telemetry through MQTT and HTTP workflows, stores normalized device state, raises alerts, and exposes APIs for monitoring dashboards. An AI engine analyzes device metrics to identify unusual reliability patterns.

Core reliability themes:

- Device health monitoring
- Telemetry lifecycle management
- Watchdog-driven recovery
- Diagnostics and fault classification
- MQTT-based messaging
- Backend alert processing
- Dashboard visibility
- AI anomaly detection
- Production-style documentation and workflow

## Architecture Summary

```text
        +-----------------------+
        | Embedded Device Sim   |
        | C++17 / Linux Threads |
        +-----------+-----------+
                    |
                    | MQTT telemetry, health, diagnostics
                    v
        +-----------------------+
        | MQTT Broker           |
        | topics / QoS / retain |
        +-----------+-----------+
                    |
                    | subscribed telemetry stream
                    v
        +-----------------------+          +----------------------+
        | Backend API           | <------> | AI Engine            |
        | FastAPI / services    |          | anomaly inference    |
        +-----------+-----------+          +----------------------+
                    |
                    | REST / WebSocket-ready APIs
                    v
        +-----------------------+
        | Monitoring Dashboard  |
        | Web demo / Qt shell   |
        +-----------------------+
```

## Engineering Goals

- Model embedded Linux device behavior using modern C++17.
- Build a clean multithreaded simulator with telemetry, watchdog, health, and recovery components.
- Use MQTT as the primary communication pattern for device-to-cloud telemetry.
- Provide a FastAPI backend with clear service boundaries.
- Design diagnostics workflows that separate detection, classification, alerting, and recovery.
- Add self-healing logic that can restart services, reset connections, or degrade gracefully.
- Introduce AI anomaly detection without coupling ML concerns into device firmware logic.
- Maintain production-style documentation, scripts, tests, and roadmap discipline.

## Target Features

- Device simulator with configurable telemetry generation
- Bounded periodic telemetry loop for local smoke testing
- Multithreaded health and watchdog loops
- MQTT publish/subscribe integration
- Optional simulator MQTT publishing mode
- Backend telemetry ingestion endpoint
- Alert and diagnostics service boundaries
- Recovery manager decision flow
- Dashboard-ready API surface
- Dashboard data contracts and operator UI shell
- AI anomaly detection placeholder pipeline
- Interactive web dashboard for local demos
- Dockerized backend and MQTT broker setup
- Unit and integration testing structure

## Tech Stack

| Layer | Technology |
| --- | --- |
| Device simulator | C++17, CMake, embedded Linux patterns |
| Messaging | MQTT, topic-based telemetry routing |
| Backend | Python, FastAPI, Pydantic |
| Dashboard | Static web dashboard, Qt architecture placeholder |
| AI engine | Python, anomaly detection pipeline |
| DevOps | Docker, PowerShell scripts |
| Testing | C++ unit test structure, Python backend tests |

## Folder Structure

```text
ring-iot-reliability-platform/
|-- ai_engine/
|-- backend/
|-- dashboard/
|-- device_simulator/
|-- docker/
|-- docs/
|-- scripts/
|-- tests/
|-- tools/
|-- README.md
|-- TODO.md
`-- .gitignore
```

## MVP Roadmap

1. Establish architecture and C++ simulator skeleton.
2. Implement device telemetry generation and health snapshots.
3. Add MQTT publishing and backend subscription flow.
4. Build diagnostics rules and alert classification.
5. Add recovery workflows and watchdog-driven self-healing.
6. Create dashboard views for fleet health and device detail.
7. Integrate anomaly detection inference.
8. Polish documentation, tests, and interview walkthrough.

## Local Demo

Run validation:

```powershell
.\scripts\test_all.ps1
```

Start the backend:

```powershell
.\scripts\run_backend.ps1 -Port 8080
```

Seed demo data:

```powershell
.\scripts\seed_demo_data.ps1 -Port 8080
```

Open the dashboard:

```powershell
Start-Process .\dashboard\web\index.html
```

Verify MQTT:

```powershell
.\scripts\verify_mqtt.ps1
```

## Reliability And Self-Healing Goals

- Detect device stalls, degraded telemetry, missed heartbeats, and resource pressure.
- Classify health states such as healthy, degraded, critical, and recovering.
- Separate monitoring from recovery decisions to keep behavior auditable.
- Record recovery attempts with reason codes and timestamps.
- Avoid automatic recovery loops without backoff and escalation logic.
- Make failure modes visible through logs, metrics, and dashboard status.

## Interview Relevance

This project is structured to support deep technical discussion around embedded systems, cloud-connected device reliability, telemetry design, multithreaded C++, backend API design, MQTT messaging, and AI-assisted monitoring.

Interviewers should be able to see:

- Clear system boundaries
- Reliability-first architecture
- Thoughtful technology choices
- Incremental implementation discipline
- Production-style documentation
- Awareness of edge/cloud tradeoffs

## Future Improvements

- Replace the in-memory event store with durable telemetry storage.
- Add WebSocket streaming for dashboard updates.
- Implement watchdog timeout simulation.
- Add Prometheus-style metrics exports.
- Add device fleet configuration files.
- Add model training data and inference validation.
- Add CI checks for C++, Python, formatting, and tests.
