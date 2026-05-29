from backend.models.dashboard import AlertState
from backend.models.events import DiagnosticsIngestRequest, DiagnosticsIngestResponse, Severity
from backend.database.store import event_repository
from backend.services.event_store import event_store


class DiagnosticsService:
    def ingest(self, payload: DiagnosticsIngestRequest) -> DiagnosticsIngestResponse:
        alert_ready = payload.severity in {Severity.WARNING, Severity.CRITICAL}
        alert = AlertState(
            device_id=payload.device_id,
            severity=payload.severity.value,
            reason_code=payload.reason_code.value,
            recommended_action=payload.recommended_action.value,
        )
        if alert_ready:
            event_store.record_alert(alert)
        event_repository.record_diagnostics(alert, payload.health_state.value)

        return DiagnosticsIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            alert_ready=alert_ready,
            message="Diagnostics event accepted for alert evaluation.",
        )
