from fastapi import APIRouter, status

from backend.models.events import DiagnosticsIngestRequest, DiagnosticsIngestResponse
from backend.services.diagnostics_service import DiagnosticsService

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])
diagnostics_service = DiagnosticsService()


@router.post(
    "/ingest",
    response_model=DiagnosticsIngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def ingest_diagnostics(payload: DiagnosticsIngestRequest) -> DiagnosticsIngestResponse:
    return diagnostics_service.ingest(payload)

