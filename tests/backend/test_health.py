from fastapi.testclient import TestClient

from backend.main import app
from backend.database.store import event_repository
from backend.services.event_store import event_store
from backend.services.auth_service import auth_service


client = TestClient(app)


def setup_function() -> None:
    event_store.clear()
    event_repository.clear()
    auth_service.clear()


def login_token() -> str:
    response = client.post(
        "/api/auth/login",
        json={"username": "operator", "password": "operator123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_system_status() -> None:
    response = client.get("/api/system/status")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database_backend"] == "sqlite"


def test_auth_login_and_me() -> None:
    token = login_token()
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"username": "operator", "role": "operator"}


def test_dashboard_snapshot_requires_session() -> None:
    response = client.get("/api/dashboard/snapshot")

    assert response.status_code == 403


def test_dashboard_history_requires_session() -> None:
    response = client.get("/api/dashboard/history")

    assert response.status_code == 403


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


def test_dashboard_snapshot_returns_live_ingested_events() -> None:
    token = login_token()
    client.post(
        "/api/telemetry/ingest",
        json={
            "device_id": "ring-sim-critical",
            "cpu_percent": 97,
            "memory_percent": 88,
            "temperature_celsius": 72,
            "uptime_seconds": 240,
        },
    )
    client.post(
        "/api/diagnostics/ingest",
        json={
            "device_id": "ring-sim-critical",
            "health_state": "critical",
            "severity": "critical",
            "reason_code": "memory_pressure",
            "recommended_action": "restart_service",
        },
    )
    client.post(
        "/api/recovery/ingest",
        json={
            "device_id": "ring-sim-critical",
            "action": "restart_service",
            "result": "started",
            "attempt": 1,
            "reason_code": "memory_pressure",
        },
    )
    client.post(
        "/api/anomaly/score",
        json={
            "device_id": "ring-sim-critical",
            "cpu_percent": 97,
            "memory_percent": 88,
            "temperature_celsius": 72,
            "uptime_seconds": 240,
        },
    )

    response = client.get(
        "/api/dashboard/snapshot",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["fleet_health"]["critical"] == 1
    assert payload["devices"][0]["device_id"] == "ring-sim-critical"
    assert payload["alerts"][0]["reason_code"] == "memory_pressure"
    assert payload["recoveries"][0]["action"] == "restart_service"
    assert payload["anomalies"][0]["is_anomaly"] is True


def test_dashboard_history_returns_persisted_events() -> None:
    token = login_token()
    client.post(
        "/api/telemetry/ingest",
        json={
            "device_id": "ring-sim-history",
            "cpu_percent": 42,
            "memory_percent": 55,
            "temperature_celsius": 38.5,
            "uptime_seconds": 120,
        },
    )
    client.post(
        "/api/diagnostics/ingest",
        json={
            "device_id": "ring-sim-history",
            "health_state": "degraded",
            "severity": "warning",
            "reason_code": "high_cpu",
            "recommended_action": "reset_network",
        },
    )
    client.post(
        "/api/recovery/ingest",
        json={
            "device_id": "ring-sim-history",
            "action": "reset_network",
            "result": "started",
            "attempt": 1,
            "reason_code": "high_cpu",
        },
    )
    client.post(
        "/api/anomaly/score",
        json={
            "device_id": "ring-sim-history",
            "cpu_percent": 84,
            "memory_percent": 61,
            "temperature_celsius": 52,
            "uptime_seconds": 180,
        },
    )

    response = client.get(
        "/api/dashboard/history?limit=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["telemetry"][0]["device_id"] == "ring-sim-history"
    assert payload["diagnostics"][0]["reason_code"] == "high_cpu"
    assert payload["recovery"][0]["action"] == "reset_network"
    assert payload["anomalies"][0]["is_anomaly"] is True
