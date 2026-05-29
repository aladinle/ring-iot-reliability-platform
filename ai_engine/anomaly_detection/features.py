from dataclasses import dataclass


@dataclass(frozen=True)
class TelemetryFeatures:
    cpu_percent: float
    memory_percent: float
    temperature_celsius: float
    uptime_seconds: int

    def as_model_input(self) -> dict[str, float]:
        return {
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "temperature_celsius": self.temperature_celsius,
            "uptime_seconds": float(self.uptime_seconds),
        }


def extract_features(payload: dict[str, float | int]) -> TelemetryFeatures:
    return TelemetryFeatures(
        cpu_percent=float(payload.get("cpu_percent", 0.0)),
        memory_percent=float(payload.get("memory_percent", 0.0)),
        temperature_celsius=float(payload.get("temperature_celsius", 0.0)),
        uptime_seconds=int(payload.get("uptime_seconds", 0)),
    )

