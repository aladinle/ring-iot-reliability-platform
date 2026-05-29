from ai_engine.inference.service import AnomalyInferenceService


def main() -> None:
    service = AnomalyInferenceService()
    score = service.score_telemetry(
        {
            "cpu_percent": 10.0,
            "memory_percent": 20.0,
            "temperature_celsius": 38.0,
            "uptime_seconds": 120,
        }
    )
    print(
        f"score={score.score} reason={score.reason} "
        f"severity={score.severity} anomaly={score.is_anomaly}"
    )


if __name__ == "__main__":
    main()
