from backend.models.diagnostics import HealthState
from backend.models.telemetry import TelemetryIngestRequest, TelemetryIngestResponse


class TelemetryService:
    def ingest(self, payload: TelemetryIngestRequest) -> TelemetryIngestResponse:
        # Future implementation: normalize, persist, evaluate diagnostics, and publish alerts.
        health_state = self._classify_health(payload)

        return TelemetryIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            health_state=health_state,
            message="Telemetry accepted for reliability evaluation.",
        )

    def _classify_health(self, payload: TelemetryIngestRequest) -> HealthState:
        if payload.cpu_percent >= 95 or payload.memory_percent >= 95:
            return HealthState.CRITICAL

        if payload.cpu_percent >= 80 or payload.memory_percent >= 80:
            return HealthState.DEGRADED

        return HealthState.HEALTHY
