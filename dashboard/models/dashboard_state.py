from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeviceStatus:
    device_id: str
    health_state: str
    cpu_percent: float
    memory_percent: float
    temperature_celsius: float
    uptime_seconds: int


@dataclass(frozen=True)
class AlertState:
    device_id: str
    severity: str
    reason_code: str
    recommended_action: str


@dataclass(frozen=True)
class RecoveryState:
    device_id: str
    action: str
    result: str
    attempt: int


@dataclass(frozen=True)
class DashboardSnapshot:
    devices: list[DeviceStatus] = field(default_factory=list)
    alerts: list[AlertState] = field(default_factory=list)
    recoveries: list[RecoveryState] = field(default_factory=list)

    def fleet_health_summary(self) -> dict[str, int]:
        summary = {"healthy": 0, "degraded": 0, "critical": 0}
        for device in self.devices:
            if device.health_state in summary:
                summary[device.health_state] += 1
        return summary

