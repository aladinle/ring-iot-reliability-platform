from dataclasses import dataclass


@dataclass(frozen=True)
class AnomalyScore:
    score: float
    reason: str


class BaselineAnomalyDetector:
    def score(self, features: dict[str, float]) -> AnomalyScore:
        # Future implementation: replace this threshold stub with trained model inference.
        cpu = features.get("cpu_percent", 0.0)
        memory = features.get("memory_percent", 0.0)

        if cpu >= 95.0 or memory >= 95.0:
            return AnomalyScore(score=0.95, reason="resource_pressure")

        return AnomalyScore(score=0.05, reason="baseline_normal")

