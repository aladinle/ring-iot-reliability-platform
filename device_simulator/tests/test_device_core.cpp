#include "Device.h"
#include "HealthMonitor.h"
#include "RecoveryManager.h"

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

    ring_iot::RecoveryManager recoveryManager;
    assert(recoveryManager.recommendAction(ring_iot::HealthState::Critical) ==
           ring_iot::RecoveryAction::RestartService);

    device.shutdown();
    assert(device.state() == ring_iot::DeviceState::Offline);

    return 0;
}
