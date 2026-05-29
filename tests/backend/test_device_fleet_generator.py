from backend.testing.device_fleet_generator import generate_test_device, generate_test_fleet


def test_generate_test_fleet_count() -> None:
    devices = generate_test_fleet(1000)

    assert len(devices) == 1000
    assert devices[0].telemetry["device_id"] == "ring-test-0001"
    assert devices[-1].telemetry["device_id"] == "ring-test-1000"


def test_generate_test_fleet_distribution() -> None:
    devices = generate_test_fleet(1000)

    critical = [device for device in devices if device.diagnostics and device.diagnostics["severity"] == "critical"]
    degraded = [device for device in devices if device.diagnostics and device.diagnostics["severity"] == "warning"]
    healthy = [device for device in devices if device.diagnostics is None]

    assert len(critical) == 50
    assert len(degraded) == 150
    assert len(healthy) == 800


def test_generate_test_device_payload_shape() -> None:
    device = generate_test_device(20)

    assert device.telemetry["device_id"] == "ring-test-0020"
    assert device.diagnostics is not None
    assert device.diagnostics["health_state"] == "critical"
    assert device.recovery is not None
    assert device.recovery["action"] == "restart_service"
    assert device.anomaly["cpu_percent"] == 97.0

