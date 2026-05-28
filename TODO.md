# 8-Week Engineering Roadmap

## Week 1: Architecture And C++ Skeleton

- Finalize repository structure.
- Document architecture, telemetry flow, and reliability goals.
- Create C++17 simulator skeleton with clear class boundaries.
- Add starter backend, dashboard, AI, Docker, and script structure.
- Establish first test directories and build commands.

## Week 2: Device Simulator

- Implement device identity, boot state, and lifecycle state machine.
- Add telemetry generation for CPU, memory, temperature, network, battery, and uptime.
- Add configurable sampling intervals.
- Add structured logging.
- Add unit tests for telemetry state transitions.

## Week 3: MQTT Communication

- Add MQTT client abstraction.
- Publish telemetry, heartbeat, diagnostics, and recovery events.
- Define topic naming convention and payload schemas.
- Add local Mosquitto broker configuration.
- Add integration test path for broker connectivity.

## Week 4: Diagnostics Engine

- Implement health rules for resource pressure, missed heartbeat, and degraded network.
- Add severity levels and diagnostic reason codes.
- Separate detection from alert dispatch.
- Add backend alert normalization.
- Add tests for rule evaluation.

## Week 5: Self-Healing Automation

- Implement recovery manager policy evaluation.
- Add simulated restart, connection reset, and safe-mode transitions.
- Add retry backoff and recovery attempt limits.
- Record recovery audit events.
- Add safeguards against recovery loops.

## Week 6: Dashboard

- Build Qt dashboard shell.
- Add fleet overview, device detail, alerts, and recovery history views.
- Connect dashboard to backend API.
- Add operator-friendly health status visualization.
- Document UI workflows.

## Week 7: AI Anomaly Detection

- Define feature extraction pipeline.
- Add baseline anomaly detection model.
- Add inference service boundary.
- Compare rule-based diagnostics with anomaly scores.
- Document model limitations and validation strategy.

## Week 8: Polish And Interview Prep

- Add final diagrams and architecture walkthrough.
- Improve README and interview talking points.
- Add representative tests and CI workflow.
- Record known limitations and future work.
- Prepare commit history and demo script.

