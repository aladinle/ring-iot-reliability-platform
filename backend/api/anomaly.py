from fastapi import APIRouter, status

from backend.models.telemetry import AnomalyScoreRequest, AnomalyScoreResponse
from backend.services.anomaly_service import AnomalyService

router = APIRouter(prefix="/anomaly", tags=["anomaly"])
anomaly_service = AnomalyService()


@router.post(
    "/score",
    response_model=AnomalyScoreResponse,
    status_code=status.HTTP_200_OK,
)
def score_anomaly(payload: AnomalyScoreRequest) -> AnomalyScoreResponse:
    return anomaly_service.score(payload)

