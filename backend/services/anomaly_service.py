from ai_engine.inference.service import AnomalyInferenceService
from backend.models.dashboard import AnomalyState
from backend.models.telemetry import AnomalyScoreRequest, AnomalyScoreResponse
from backend.database.store import event_repository
from backend.services.event_store import event_store


class AnomalyService:
    def __init__(self) -> None:
        self.inference = AnomalyInferenceService()

    def score(self, payload: AnomalyScoreRequest) -> AnomalyScoreResponse:
        score = self.inference.score_telemetry(
            {
                "cpu_percent": payload.cpu_percent,
                "memory_percent": payload.memory_percent,
                "temperature_celsius": payload.temperature_celsius,
                "uptime_seconds": payload.uptime_seconds,
            }
        )

        response = AnomalyScoreResponse(
            device_id=payload.device_id,
            score=score.score,
            reason=score.reason,
            severity=score.severity,
            is_anomaly=score.is_anomaly,
        )
        anomaly = AnomalyState(
            device_id=response.device_id,
            score=response.score,
            reason=response.reason,
            severity=response.severity,
            is_anomaly=response.is_anomaly,
        )
        event_store.record_anomaly(anomaly)
        event_repository.record_anomaly(anomaly)
        return response
