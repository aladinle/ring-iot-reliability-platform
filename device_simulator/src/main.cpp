#include "DeviceConfig.h"
#include "Device.h"
#include "HealthMonitor.h"
#include "RecoveryManager.h"
#include "TelemetryManager.h"
#include "TelemetrySerializer.h"
#include "Watchdog.h"

#include <chrono>
#include <iostream>
#include <thread>

int main(int argc, char* argv[]) {
    const std::string configPath = argc > 1 ? argv[1] : "device_simulator/config/device_config.example.json";
    const auto config = ring_iot::loadDeviceConfig(configPath);

    ring_iot::Device device(config.deviceId);
    ring_iot::TelemetryProfile profile;
    profile.baselineCpuPercent = config.baselineCpuPercent;
    profile.baselineMemoryPercent = config.baselineMemoryPercent;
    profile.baselineTemperatureCelsius = config.baselineTemperatureCelsius;

    ring_iot::TelemetryManager telemetry(device.id(), profile);
    ring_iot::HealthMonitor healthMonitor;
    ring_iot::RecoveryManager recoveryManager;
    ring_iot::Watchdog watchdog(std::chrono::duration_cast<std::chrono::seconds>(config.watchdogTimeout));

    device.boot();
    watchdog.markHeartbeat();

    std::cout << "Device simulator skeleton initialized for " << device.id() << '\n';

    for (int sampleIndex = 0; sampleIndex < config.sampleCount; ++sampleIndex) {
        const auto snapshot = telemetry.collectSnapshot();
        const auto health = healthMonitor.evaluate(snapshot);
        const auto action = recoveryManager.recommendAction(health);
        recoveryManager.recordAttempt(action);
        watchdog.markHeartbeat();

        std::cout << serializeTelemetryJson(snapshot, config.siteId, "2026-05-28T17:00:00Z") << '\n';

        if (sampleIndex + 1 < config.sampleCount) {
            std::this_thread::sleep_for(config.telemetryInterval);
        }
    }

    device.shutdown();

    return 0;
}
