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

- Implement health rules for resource pressure and thermal pressure. `[done]`
- Add severity levels and diagnostic reason codes. `[done]`
- Separate detection from alert dispatch. `[done]`
- Add backend diagnostics ingestion. `[done]`
- Add tests for rule evaluation. `[done]`
- Future enhancement: missed heartbeat and degraded network rules.

## Week 5: Self-Healing Automation

- Implement recovery manager policy evaluation. `[done]`
- Add simulated restart, connection reset, and safe-mode transitions. `[done]`
- Add recovery attempt limits. `[done]`
- Record recovery audit events. `[done]`
- Add backend recovery ingestion. `[done]`
- Future enhancement: time-based retry backoff and persistent recovery history.

## Week 6: Dashboard

- Build Qt dashboard shell. `[done]`
- Add fleet overview data model. `[done]`
- Add alerts and recovery history data models. `[done]`
- Connect dashboard support layer to backend health API. `[done]`
- Add operator-friendly mock snapshot and tests. `[done]`
- Future enhancement: full Qt build integration and live backend polling.

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
