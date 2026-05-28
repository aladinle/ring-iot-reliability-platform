#pragma once

#include "TelemetryManager.h"

namespace ring_iot {

enum class HealthState {
    Healthy,
    Degraded,
    Critical
};

class HealthMonitor {
public:
    HealthState evaluate(const TelemetrySnapshot& snapshot) const;
};

} // namespace ring_iot

