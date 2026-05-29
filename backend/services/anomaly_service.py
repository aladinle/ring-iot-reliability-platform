from ai_engine.inference.service import AnomalyInferenceService
from backend.models.telemetry import AnomalyScoreRequest, AnomalyScoreResponse


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

        return AnomalyScoreResponse(
            device_id=payload.device_id,
            score=score.score,
            reason=score.reason,
            severity=score.severity,
            is_anomaly=score.is_anomaly,
        )

