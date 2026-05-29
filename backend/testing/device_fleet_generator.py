from dataclasses import dataclass
from urllib.request import Request, urlopen
import json


@dataclass(frozen=True)
class GeneratedDevice:
    telemetry: dict[str, float | int | str]
    diagnostics: dict[str, str] | None
    recovery: dict[str, int | str] | None
    anomaly: dict[str, float | int | str]


def generate_test_device(index: int) -> GeneratedDevice:
    device_id = f"ring-test-{index:04d}"
    uptime = 120 + index

    if index % 20 == 0:
        cpu = 97.0
        memory = 88.0
        temperature = 72.0
        diagnostics = {
            "device_id": device_id,
            "health_state": "critical",
            "severity": "critical",
            "reason_code": "memory_pressure",
            "recommended_action": "restart_service",
        }
        recovery = {
            "device_id": device_id,
            "action": "restart_service",
            "result": "started",
            "attempt": 1,
            "reason_code": "memory_pressure",
        }
    elif index % 5 == 0:
        cpu = 84.0
        memory = 61.0
        temperature = 52.0
        diagnostics = {
            "device_id": device_id,
            "health_state": "degraded",
            "severity": "warning",
            "reason_code": "high_cpu",
            "recommended_action": "reset_network",
        }
        recovery = {
            "device_id": device_id,
            "action": "reset_network",
            "result": "started",
            "attempt": 1,
            "reason_code": "high_cpu",
        }
    else:
        cpu = 20.0 + float(index % 30)
        memory = 35.0 + float(index % 25)
        temperature = 36.0 + float(index % 8)
        diagnostics = None
        recovery = None

    telemetry = {
        "device_id": device_id,
        "cpu_percent": cpu,
        "memory_percent": memory,
        "temperature_celsius": temperature,
        "uptime_seconds": uptime,
    }

    return GeneratedDevice(
        telemetry=telemetry,
        diagnostics=diagnostics,
        recovery=recovery,
        anomaly=telemetry,
    )


def generate_test_fleet(count: int) -> list[GeneratedDevice]:
    if count < 1:
        raise ValueError("count must be positive")
    return [generate_test_device(index) for index in range(1, count + 1)]


def post_json(base_url: str, path: str, payload: dict[str, object]) -> None:
    request = Request(
        f"{base_url.rstrip('/')}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=10) as response:
        response.read()


def seed_fleet(base_url: str, count: int) -> None:
    for generated in generate_test_fleet(count):
        post_json(base_url, "/api/telemetry/ingest", generated.telemetry)
        if generated.diagnostics is not None:
            post_json(base_url, "/api/diagnostics/ingest", generated.diagnostics)
        if generated.recovery is not None:
            post_json(base_url, "/api/recovery/ingest", generated.recovery)
        post_json(base_url, "/api/anomaly/score", generated.anomaly)

