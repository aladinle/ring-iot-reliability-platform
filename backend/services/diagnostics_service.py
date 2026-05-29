from backend.models.dashboard import AlertState
from backend.models.events import DiagnosticsIngestRequest, DiagnosticsIngestResponse, Severity
from backend.services.event_store import event_store


class DiagnosticsService:
    def ingest(self, payload: DiagnosticsIngestRequest) -> DiagnosticsIngestResponse:
        alert_ready = payload.severity in {Severity.WARNING, Severity.CRITICAL}
        if alert_ready:
            event_store.record_alert(
                AlertState(
                    device_id=payload.device_id,
                    severity=payload.severity.value,
                    reason_code=payload.reason_code.value,
                    recommended_action=payload.recommended_action.value,
                )
            )

        return DiagnosticsIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            alert_ready=alert_ready,
            message="Diagnostics event accepted for alert evaluation.",
        )
