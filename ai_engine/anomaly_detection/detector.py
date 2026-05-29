from dataclasses import dataclass


@dataclass(frozen=True)
class AnomalyScore:
    score: float
    reason: str
    severity: str
    is_anomaly: bool


class BaselineAnomalyDetector:
    def score(self, features: dict[str, float]) -> AnomalyScore:
        # Baseline model: deterministic weighted rules until real training data exists.
        cpu = features.get("cpu_percent", 0.0)
        memory = features.get("memory_percent", 0.0)
        temperature = features.get("temperature_celsius", 0.0)

        weighted_score = max(
            cpu / 100.0,
            memory / 100.0,
            max(0.0, (temperature - 35.0) / 60.0),
        )

        if cpu >= 95.0 or memory >= 95.0 or temperature >= 85.0:
            return AnomalyScore(
                score=max(0.95, weighted_score),
                reason="critical_resource_pressure",
                severity="critical",
                is_anomaly=True,
            )

        if cpu >= 80.0 or memory >= 80.0 or temperature >= 75.0:
            return AnomalyScore(
                score=max(0.65, weighted_score),
                reason="degraded_resource_pattern",
                severity="warning",
                is_anomaly=True,
            )

        return AnomalyScore(
            score=min(0.30, weighted_score),
            reason="baseline_normal",
            severity="info",
            is_anomaly=False,
        )
