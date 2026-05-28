#pragma once

#include <chrono>
#include <string>

namespace ring_iot {

struct TelemetrySnapshot {
    std::string deviceId;
    double cpuPercent = 0.0;
    double memoryPercent = 0.0;
    double temperatureCelsius = 0.0;
    std::chrono::seconds uptime{0};
};

struct TelemetryProfile {
    double baselineCpuPercent = 12.0;
    double baselineMemoryPercent = 34.0;
    double baselineTemperatureCelsius = 41.0;
};

class TelemetryManager {
public:
    explicit TelemetryManager(std::string deviceId);
    TelemetryManager(std::string deviceId, TelemetryProfile profile);

    TelemetrySnapshot collectSnapshot() const;

private:
    std::string deviceId_;
    TelemetryProfile profile_;
    std::chrono::steady_clock::time_point startedAt_;
};

} // namespace ring_iot
