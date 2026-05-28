# 8-Week Engineering Roadmap

## Week 1: Architecture And C++ Skeleton

- Finalize repository structure.
- Document architecture, telemetry flow, and reliability goals.
- Create C++17 simulator skeleton with clear class boundaries.
- Add starter backend, dashboard, AI, Docker, and script structure.
- Establish first test directories and build commands.

## Week 2: Device Simulator

- Implement device identity, boot state, and lifecycle state machine. `[done]`
- Add telemetry generation for CPU, memory, temperature, and uptime. `[done]`
- Add configurable sampling intervals and bounded sample count. `[done]`
- Add diagnostics output for degraded and critical scenarios. `[done]`
- Add recovery recommendations for degraded and critical health states. `[done]`
- Add unit tests for telemetry, config loading, diagnostics, and recovery recommendations. `[done]`
- Future enhancement: add network, battery, and structured log sinks.

## Week 3: MQTT Communication

- Add MQTT client abstraction. `[done]`
- Publish telemetry and diagnostics events. `[done]`
- Define topic naming convention and payload schemas. `[done]`
- Add local Mosquitto broker configuration. `[done]`
- Add integration smoke test path for broker connectivity. `[done]`
- Future enhancement: heartbeat and recovery event publishing.
- Future enhancement: TLS, authentication, reconnect backoff, and QoS policy.

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
