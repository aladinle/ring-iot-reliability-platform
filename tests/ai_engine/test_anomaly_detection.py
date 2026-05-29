from ai_engine.inference.service import AnomalyInferenceService


def test_anomaly_service_scores_normal_telemetry() -> None:
    service = AnomalyInferenceService()

    score = service.score_telemetry(
        {
            "cpu_percent": 24,
            "memory_percent": 48,
            "temperature_celsius": 39.5,
            "uptime_seconds": 120,
        }
    )

    assert score.is_anomaly is False
    assert score.severity == "info"
    assert score.reason == "baseline_normal"


def test_anomaly_service_scores_degraded_telemetry() -> None:
    service = AnomalyInferenceService()

    score = service.score_telemetry(
        {
            "cpu_percent": 84,
            "memory_percent": 61,
            "temperature_celsius": 52,
            "uptime_seconds": 180,
        }
    )

    assert score.is_anomaly is True
    assert score.severity == "warning"
    assert score.reason == "degraded_resource_pattern"


def test_anomaly_service_scores_critical_telemetry() -> None:
    service = AnomalyInferenceService()

    score = service.score_telemetry(
        {
            "cpu_percent": 97,
            "memory_percent": 88,
            "temperature_celsius": 72,
            "uptime_seconds": 240,
        }
    )

    assert score.is_anomaly is True
    assert score.severity == "critical"
    assert score.reason == "critical_resource_pressure"
