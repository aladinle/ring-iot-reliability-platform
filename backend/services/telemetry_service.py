from backend.models.diagnostics import HealthState
from backend.models.dashboard import DeviceStatus
from backend.models.telemetry import TelemetryIngestRequest, TelemetryIngestResponse
from backend.database.store import event_repository
from backend.services.event_store import event_store


class TelemetryService:
    def ingest(self, payload: TelemetryIngestRequest) -> TelemetryIngestResponse:
        health_state = self._classify_health(payload)
        device = DeviceStatus(
            device_id=payload.device_id,
            health_state=health_state.value,
            cpu_percent=payload.cpu_percent,
            memory_percent=payload.memory_percent,
            temperature_celsius=payload.temperature_celsius,
            uptime_seconds=payload.uptime_seconds,
        )
        event_store.record_device(device)
        event_repository.record_telemetry(device)

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
