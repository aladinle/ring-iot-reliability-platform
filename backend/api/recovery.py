from fastapi import APIRouter, status

from backend.models.events import RecoveryIngestRequest, RecoveryIngestResponse
from backend.services.recovery_service import RecoveryService

router = APIRouter(prefix="/recovery", tags=["recovery"])
recovery_service = RecoveryService()


@router.post(
    "/ingest",
    response_model=RecoveryIngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def ingest_recovery(payload: RecoveryIngestRequest) -> RecoveryIngestResponse:
    return recovery_service.ingest(payload)

