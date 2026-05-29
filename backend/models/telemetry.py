from datetime import datetime, timezone

from pydantic import BaseModel, Field


class TelemetryIngestRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    cpu_percent: float = Field(..., ge=0, le=100)
    memory_percent: float = Field(..., ge=0, le=100)
    temperature_celsius: float
    uptime_seconds: int = Field(..., ge=0)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TelemetryIngestResponse(BaseModel):
    accepted: bool
    device_id: str
    health_state: str
    message: str


class AnomalyScoreRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    cpu_percent: float = Field(..., ge=0, le=100)
    memory_percent: float = Field(..., ge=0, le=100)
    temperature_celsius: float
    uptime_seconds: int = Field(..., ge=0)


class AnomalyScoreResponse(BaseModel):
    device_id: str
    score: float = Field(..., ge=0, le=1)
    reason: str
    severity: str
    is_anomaly: bool
