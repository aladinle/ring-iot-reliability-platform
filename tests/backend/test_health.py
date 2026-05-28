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
