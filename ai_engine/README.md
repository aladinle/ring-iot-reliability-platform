# AI Engine

The AI engine will provide anomaly detection for device telemetry and reliability signals.

It is intentionally isolated from the backend ingestion path so early diagnostics can stay explainable and deterministic. Future inference can run asynchronously or behind an internal API.

