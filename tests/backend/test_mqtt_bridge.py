from backend.telemetry.mqtt_bridge import encode_remaining_length, route_mqtt_event


def test_route_mqtt_telemetry_event() -> None:
    routed = route_mqtt_event(
        "devices/ring-sim-001/telemetry",
        {
            "device_id": "ring-sim-001",
            "metrics": {
                "cpu_percent": 42,
                "memory_percent": 55,
                "temperature_celsius": 38.5,
                "uptime_seconds": 120,
            },
        },
    )

    assert routed is not None
    path, body = routed
    assert path == "/api/telemetry/ingest"
    assert body["device_id"] == "ring-sim-001"
    assert body["cpu_percent"] == 42


def test_route_mqtt_diagnostics_event() -> None:
    routed = route_mqtt_event(
        "devices/ring-sim-001/diagnostics",
        {
            "device_id": "ring-sim-001",
            "health_state": "degraded",
            "severity": "warning",
            "reason_code": "high_cpu",
            "recommended_action": "reset_network",
        },
    )

    assert routed is not None
    assert routed[0] == "/api/diagnostics/ingest"
    assert routed[1]["recommended_action"] == "reset_network"


def test_route_mqtt_recovery_event() -> None:
    routed = route_mqtt_event(
        "devices/ring-sim-001/recovery",
        {
            "device_id": "ring-sim-001",
            "action": "reset_network",
            "result": "started",
            "attempt": 1,
            "reason_code": "high_cpu",
        },
    )

    assert routed is not None
    assert routed[0] == "/api/recovery/ingest"
    assert routed[1]["attempt"] == 1


def test_encode_remaining_length() -> None:
    assert encode_remaining_length(127) == b"\x7f"
    assert encode_remaining_length(128) == b"\x80\x01"
