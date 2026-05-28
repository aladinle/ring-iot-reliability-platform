#include "TelemetryManager.h"

#include <utility>

namespace ring_iot {

TelemetryManager::TelemetryManager(std::string deviceId)
    : TelemetryManager(std::move(deviceId), TelemetryProfile{}) {}

TelemetryManager::TelemetryManager(std::string deviceId, TelemetryProfile profile)
    : deviceId_(std::move(deviceId)),
      profile_(profile),
      startedAt_(std::chrono::steady_clock::now()) {}

TelemetrySnapshot TelemetryManager::collectSnapshot() const {
    // Future implementation: replace deterministic profile values with /proc, sysfs, or scenario-driven inputs.
    TelemetrySnapshot snapshot;
    snapshot.deviceId = deviceId_;
    snapshot.cpuPercent = profile_.baselineCpuPercent;
    snapshot.memoryPercent = profile_.baselineMemoryPercent;
    snapshot.temperatureCelsius = profile_.baselineTemperatureCelsius;
    snapshot.uptime = std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::steady_clock::now() - startedAt_);
    return snapshot;
}

} // namespace ring_iot
