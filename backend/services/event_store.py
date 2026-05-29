from threading import Lock

from backend.models.dashboard import (
    AlertState,
    AnomalyState,
    DashboardSnapshotResponse,
    DeviceStatus,
    RecoveryState,
)


class EventStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._devices: dict[str, DeviceStatus] = {}
        self._alerts: list[AlertState] = []
        self._recoveries: list[RecoveryState] = []
        self._anomalies: list[AnomalyState] = []

    def clear(self) -> None:
        with self._lock:
            self._devices.clear()
            self._alerts.clear()
            self._recoveries.clear()
            self._anomalies.clear()

    def record_device(self, device: DeviceStatus) -> None:
        with self._lock:
            self._devices[device.device_id] = device

    def record_alert(self, alert: AlertState) -> None:
        with self._lock:
            self._alerts.append(alert)
            self._alerts = self._alerts[-50:]

    def record_recovery(self, recovery: RecoveryState) -> None:
        with self._lock:
            self._recoveries.append(recovery)
            self._recoveries = self._recoveries[-50:]

    def record_anomaly(self, anomaly: AnomalyState) -> None:
        with self._lock:
            self._anomalies.append(anomaly)
            self._anomalies = self._anomalies[-50:]

    def snapshot(self) -> DashboardSnapshotResponse:
        with self._lock:
            devices = list(self._devices.values())
            fleet_health = {"healthy": 0, "degraded": 0, "critical": 0}
            for device in devices:
                if device.health_state in fleet_health:
                    fleet_health[device.health_state] += 1

            return DashboardSnapshotResponse(
                fleet_health=fleet_health,
                devices=devices,
                alerts=list(self._alerts),
                recoveries=list(self._recoveries),
                anomalies=list(self._anomalies),
            )


event_store = EventStore()

