from pydantic import BaseModel


class DeviceStatus(BaseModel):
    device_id: str
    health_state: str
    cpu_percent: float
    memory_percent: float
    temperature_celsius: float
    uptime_seconds: int


class AlertState(BaseModel):
    device_id: str
    severity: str
    reason_code: str
    recommended_action: str


class RecoveryState(BaseModel):
    device_id: str
    action: str
    result: str
    attempt: int


class AnomalyState(BaseModel):
    device_id: str
    score: float
    reason: str
    severity: str
    is_anomaly: bool


class DashboardSnapshotResponse(BaseModel):
    fleet_health: dict[str, int]
    devices: list[DeviceStatus]
    alerts: list[AlertState]
    recoveries: list[RecoveryState]
    anomalies: list[AnomalyState]

