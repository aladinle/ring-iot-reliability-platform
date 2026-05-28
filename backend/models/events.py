from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class HealthState(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ReasonCode(StrEnum):
    NORMAL = "normal"
    HIGH_CPU = "high_cpu"
    MEMORY_PRESSURE = "memory_pressure"
    THERMAL_PRESSURE = "thermal_pressure"
    HEARTBEAT_TIMEOUT = "heartbeat_timeout"
    TELEMETRY_STALE = "telemetry_stale"
    REPEATED_RECOVERY = "repeated_recovery"


class RecoveryAction(StrEnum):
    NONE = "none"
    RESET_NETWORK = "reset_network"
    RESTART_SERVICE = "restart_service"
    ENTER_SAFE_MODE = "enter_safe_mode"


class DiagnosticsIngestRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    health_state: HealthState
    severity: Severity
    reason_code: ReasonCode
    recommended_action: RecoveryAction
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DiagnosticsIngestResponse(BaseModel):
    accepted: bool
    device_id: str
    alert_ready: bool
    message: str


class RecoveryResult(StrEnum):
    SKIPPED = "skipped"
    STARTED = "started"
    SUPPRESSED = "suppressed"


class RecoveryIngestRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    action: RecoveryAction
    result: RecoveryResult
    attempt: int = Field(..., ge=0)
    reason_code: ReasonCode
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RecoveryIngestResponse(BaseModel):
    accepted: bool
    device_id: str
    recovery_recorded: bool
    message: str

