from fastapi import APIRouter, status

from backend.models.telemetry import TelemetryIngestRequest, TelemetryIngestResponse
from backend.services.telemetry_service import TelemetryService

router = APIRouter(prefix="/telemetry", tags=["telemetry"])
telemetry_service = TelemetryService()


@router.post(
    "/ingest",
    response_model=TelemetryIngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def ingest_telemetry(payload: TelemetryIngestRequest) -> TelemetryIngestResponse:
    return telemetry_service.ingest(payload)
