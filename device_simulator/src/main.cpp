#include "Device.h"
#include "HealthMonitor.h"
#include "RecoveryManager.h"
#include "TelemetryManager.h"
#include "Watchdog.h"

#include <chrono>
#include <iostream>

int main() {
    ring_iot::Device device("ring-sim-001");
    ring_iot::TelemetryProfile profile;
    profile.baselineCpuPercent = 24.0;
    profile.baselineMemoryPercent = 48.0;
    profile.baselineTemperatureCelsius = 39.5;

    ring_iot::TelemetryManager telemetry(device.id(), profile);
    ring_iot::HealthMonitor healthMonitor;
    ring_iot::RecoveryManager recoveryManager;
    ring_iot::Watchdog watchdog(std::chrono::seconds(30));

    device.boot();
    watchdog.markHeartbeat();

    const auto snapshot = telemetry.collectSnapshot();
    const auto health = healthMonitor.evaluate(snapshot);
    const auto action = recoveryManager.recommendAction(health);
    recoveryManager.recordAttempt(action);

    std::cout << "Device simulator skeleton initialized for " << device.id() << '\n';
    std::cout << "Telemetry snapshot cpu=" << snapshot.cpuPercent
              << "% memory=" << snapshot.memoryPercent
              << "% temperature=" << snapshot.temperatureCelsius << "C\n";
    device.shutdown();

    return 0;
}
