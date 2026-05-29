from typing import Protocol

from backend.models.dashboard import AlertState, AnomalyState, DeviceStatus, RecoveryState


class EventRepository(Protocol):
    def initialize(self) -> None:
        ...

    def clear(self) -> None:
        ...

    def record_telemetry(self, device: DeviceStatus) -> None:
        ...

    def record_diagnostics(self, alert: AlertState, health_state: str) -> None:
        ...

    def record_recovery(self, recovery: RecoveryState, reason_code: str) -> None:
        ...

    def record_anomaly(self, anomaly: AnomalyState) -> None:
        ...

    def history(self, limit: int = 100) -> dict[str, list[dict[str, object]]]:
        ...

