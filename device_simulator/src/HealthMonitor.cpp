#include "HealthMonitor.h"

namespace ring_iot {

HealthState HealthMonitor::evaluate(const TelemetrySnapshot& snapshot) const {
    // Future implementation: evaluate configurable thresholds and emit reason codes.
    if (snapshot.cpuPercent >= 95.0 || snapshot.memoryPercent >= 95.0 ||
        snapshot.temperatureCelsius >= 85.0) {
        return HealthState::Critical;
    }

    if (snapshot.cpuPercent >= 80.0 || snapshot.memoryPercent >= 80.0 ||
        snapshot.temperatureCelsius >= 75.0) {
        return HealthState::Degraded;
    }

    return HealthState::Healthy;
}

} // namespace ring_iot
