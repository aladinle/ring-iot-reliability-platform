from ai_engine.anomaly_detection.detector import AnomalyScore, BaselineAnomalyDetector
from ai_engine.anomaly_detection.features import extract_features


class AnomalyInferenceService:
    def __init__(self, detector: BaselineAnomalyDetector | None = None) -> None:
        self.detector = detector or BaselineAnomalyDetector()

    def score_telemetry(self, telemetry: dict[str, float | int]) -> AnomalyScore:
        features = extract_features(telemetry)
        return self.detector.score(features.as_model_input())

