from backend.models.events import DiagnosticsIngestRequest, DiagnosticsIngestResponse, Severity


class DiagnosticsService:
    def ingest(self, payload: DiagnosticsIngestRequest) -> DiagnosticsIngestResponse:
        # Future implementation: persist diagnostics, deduplicate alerts, and route critical events.
        alert_ready = payload.severity in {Severity.WARNING, Severity.CRITICAL}

        return DiagnosticsIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            alert_ready=alert_ready,
            message="Diagnostics event accepted for alert evaluation.",
        )

