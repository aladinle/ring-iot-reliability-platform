from backend.models.dashboard import RecoveryState
from backend.models.events import RecoveryIngestRequest, RecoveryIngestResponse, RecoveryResult
from backend.database.store import event_repository
from backend.services.event_store import event_store


class RecoveryService:
    def ingest(self, payload: RecoveryIngestRequest) -> RecoveryIngestResponse:
        recovery_recorded = payload.result == RecoveryResult.STARTED
        recovery = RecoveryState(
            device_id=payload.device_id,
            action=payload.action.value,
            result=payload.result.value,
            attempt=payload.attempt,
        )
        event_store.record_recovery(recovery)
        event_repository.record_recovery(recovery, payload.reason_code.value)

        return RecoveryIngestResponse(
            accepted=True,
            device_id=payload.device_id,
            recovery_recorded=recovery_recorded,
            message="Recovery event accepted for audit history.",
        )
