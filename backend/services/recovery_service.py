from backend.models.dashboard import RecoveryState
from backend.models.events import RecoveryIngestRequest, RecoveryIngestResponse, RecoveryResult
from backend.services.event_store import event_store


class RecoveryService:
    def ingest(self, payload: RecoveryIngestRequest) -> RecoveryIngestResponse:
        recovery_recorded = payload.result == RecoveryResult.STARTED
        event_store.record_recovery(
            RecoveryState(
                device_id=payload.device_id,
                action=payload.action.value,
                result=payload.result.value,
                attempt=payload.attempt,
            )
        )

        return RecoveryIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            recovery_recorded=recovery_recorded,
            message="Recovery event accepted for audit history.",
        )
