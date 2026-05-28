from backend.models.events import RecoveryIngestRequest, RecoveryIngestResponse, RecoveryResult


class RecoveryService:
    def ingest(self, payload: RecoveryIngestRequest) -> RecoveryIngestResponse:
        # Future implementation: persist recovery history and detect repeated recovery loops.
        recovery_recorded = payload.result == RecoveryResult.STARTED

        return RecoveryIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            recovery_recorded=recovery_recorded,
            message="Recovery event accepted for audit history.",
        )

