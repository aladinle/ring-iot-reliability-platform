import json

from dashboard.services.api_client import DashboardApiClient


def test_dashboard_mock_snapshot_summarizes_fleet_health() -> None:
    client = DashboardApiClient("http://127.0.0.1:8080")
    snapshot = client.build_mock_snapshot()

    assert snapshot.fleet_health_summary() == {
        "healthy": 1,
        "degraded": 0,
        "critical": 1,
    }


def test_dashboard_snapshot_serializes_to_json() -> None:
    client = DashboardApiClient("http://127.0.0.1:8080")
    payload = json.loads(client.snapshot_as_json(client.build_mock_snapshot()))

    assert payload["fleet_health"]["critical"] == 1
    assert payload["alerts"][0]["recommended_action"] == "restart_service"
    assert payload["recoveries"][0]["result"] == "started"

