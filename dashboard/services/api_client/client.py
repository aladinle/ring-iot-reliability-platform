import json
from dataclasses import asdict
from urllib.error import URLError
from urllib.request import Request, urlopen

from dashboard.models.dashboard_state import AlertState, DashboardSnapshot, DeviceStatus, RecoveryState


class DashboardApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict[str, str]:
        return self._get_json("/health")

    def build_mock_snapshot(self) -> DashboardSnapshot:
        return DashboardSnapshot(
            devices=[
                DeviceStatus(
                    device_id="ring-sim-healthy",
                    health_state="healthy",
                    cpu_percent=24.0,
                    memory_percent=48.0,
                    temperature_celsius=39.5,
                    uptime_seconds=120,
                ),
                DeviceStatus(
                    device_id="ring-sim-critical",
                    health_state="critical",
                    cpu_percent=97.0,
                    memory_percent=88.0,
                    temperature_celsius=72.0,
                    uptime_seconds=240,
                ),
            ],
            alerts=[
                AlertState(
                    device_id="ring-sim-critical",
                    severity="critical",
                    reason_code="memory_pressure",
                    recommended_action="restart_service",
                )
            ],
            recoveries=[
                RecoveryState(
                    device_id="ring-sim-critical",
                    action="restart_service",
                    result="started",
                    attempt=1,
                )
            ],
        )

    def snapshot_as_json(self, snapshot: DashboardSnapshot) -> str:
        return json.dumps(
            {
                "devices": [asdict(device) for device in snapshot.devices],
                "alerts": [asdict(alert) for alert in snapshot.alerts],
                "recoveries": [asdict(recovery) for recovery in snapshot.recoveries],
                "fleet_health": snapshot.fleet_health_summary(),
            },
            sort_keys=True,
        )

    def _get_json(self, path: str) -> dict[str, str]:
        request = Request(f"{self.base_url}{path}", method="GET")
        try:
            with urlopen(request, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))
        except URLError as exc:
            raise RuntimeError(f"Dashboard API request failed: {exc}") from exc

