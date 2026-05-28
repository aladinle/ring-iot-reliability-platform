#include "DeviceConfig.h"
#include "Device.h"
#include "HealthMonitor.h"
#include "RecoveryManager.h"
#include "TelemetrySerializer.h"

#include <cassert>

int main() {
    ring_iot::Device device("test-device");
    assert(device.state() == ring_iot::DeviceState::Offline);

    device.boot();
    assert(device.state() == ring_iot::DeviceState::Healthy);

    ring_iot::TelemetrySnapshot snapshot;
    snapshot.cpuPercent = 96.0;

    ring_iot::HealthMonitor healthMonitor;
    assert(healthMonitor.evaluate(snapshot) == ring_iot::HealthState::Critical);

    ring_iot::TelemetryProfile profile;
    profile.baselineCpuPercent = 22.0;
    profile.baselineMemoryPercent = 33.0;
    profile.baselineTemperatureCelsius = 44.0;

    ring_iot::TelemetryManager telemetry(device.id(), profile);
    const auto collected = telemetry.collectSnapshot();
    assert(collected.deviceId == "test-device");
    assert(collected.cpuPercent == 22.0);
    assert(collected.memoryPercent == 33.0);
    assert(collected.temperatureCelsius == 44.0);

    const auto config = ring_iot::loadDeviceConfig("tests/fixtures/device_config.test.json");
    assert(config.deviceId == "ring-test-001");
    assert(config.siteId == "test-lab");
    assert(config.telemetryInterval.count() == 250);
    assert(config.watchdogTimeout.count() == 5000);
    assert(config.sampleCount == 2);
    assert(config.baselineCpuPercent == 11.5);
    assert(config.baselineMemoryPercent == 22.5);
    assert(config.baselineTemperatureCelsius == 33.5);

    const auto payload = ring_iot::serializeTelemetryJson(collected, "test-lab", "2026-05-28T17:00:00Z");
    assert(payload.find("\"schema_version\":\"1.0\"") != std::string::npos);
    assert(payload.find("\"device_id\":\"test-device\"") != std::string::npos);
    assert(payload.find("\"site_id\":\"test-lab\"") != std::string::npos);
    assert(payload.find("\"cpu_percent\":22") != std::string::npos);

    ring_iot::RecoveryManager recoveryManager;
    assert(recoveryManager.recommendAction(ring_iot::HealthState::Critical) ==
           ring_iot::RecoveryAction::RestartService);

    device.shutdown();
    assert(device.state() == ring_iot::DeviceState::Offline);

    return 0;
}
