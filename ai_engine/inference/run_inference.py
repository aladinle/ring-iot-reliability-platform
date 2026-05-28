from anomaly_detection.detector import BaselineAnomalyDetector


def main() -> None:
    detector = BaselineAnomalyDetector()
    score = detector.score({"cpu_percent": 10.0, "memory_percent": 20.0})
    print(f"score={score.score} reason={score.reason}")


if __name__ == "__main__":
    main()

