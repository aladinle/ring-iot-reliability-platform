from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_telemetry_ingest_returns_healthy_state() -> None:
    response = client.post(
        "/api/telemetry/ingest",
        json={
            "device_id": "ring-sim-001",
            "cpu_percent": 42,
            "memory_percent": 55,
            "temperature_celsius": 38.5,
            "uptime_seconds": 120,
        },
    )

    assert response.status_code == 202
    assert response.json()["accepted"] is True
    assert response.json()["health_state"] == "healthy"


def test_telemetry_ingest_returns_degraded_state() -> None:
    response = client.post(
        "/api/telemetry/ingest",
        json={
            "device_id": "ring-sim-001",
            "cpu_percent": 81,
            "memory_percent": 55,
            "temperature_celsius": 41.0,
            "uptime_seconds": 240,
        },
    )

    assert response.status_code == 202
    assert response.json()["health_state"] == "degraded"


def test_telemetry_ingest_returns_critical_state() -> None:
    response = client.post(
        "/api/telemetry/ingest",
        json={
            "device_id": "ring-sim-001",
            "cpu_percent": 42,
            "memory_percent": 96,
            "temperature_celsius": 50.0,
            "uptime_seconds": 360,
        },
    )

    assert response.status_code == 202
    assert response.json()["health_state"] == "critical"


def test_diagnostics_ingest_accepts_alert_ready_event() -> None:
    response = client.post(
        "/api/diagnostics/ingest",
        json={
            "device_id": "ring-sim-critical",
            "health_state": "critical",
            "severity": "critical",
            "reason_code": "memory_pressure",
            "recommended_action": "restart_service",
        },
    )

    assert response.status_code == 202
    assert response.json()["accepted"] is True
    assert response.json()["alert_ready"] is True


def test_recovery_ingest_records_started_recovery() -> None:
    response = client.post(
        "/api/recovery/ingest",
        json={
            "device_id": "ring-sim-critical",
            "action": "restart_service",
            "result": "started",
            "attempt": 1,
            "reason_code": "memory_pressure",
        },
    )

    assert response.status_code == 202
    assert response.json()["accepted"] is True
    assert response.json()["recovery_recorded"] is True


def test_anomaly_score_returns_warning_for_degraded_telemetry() -> None:
    response = client.post(
        "/api/anomaly/score",
        json={
            "device_id": "ring-sim-degraded",
            "cpu_percent": 84,
            "memory_percent": 61,
            "temperature_celsius": 52,
            "uptime_seconds": 180,
        },
    )

    assert response.status_code == 200
    assert response.json()["device_id"] == "ring-sim-degraded"
    assert response.json()["is_anomaly"] is True
    assert response.json()["severity"] == "warning"
