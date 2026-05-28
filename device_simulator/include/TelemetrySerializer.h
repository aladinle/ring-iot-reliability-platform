#pragma once

#include "TelemetryManager.h"

#include <string>

namespace ring_iot {

std::string serializeTelemetryJson(
    const TelemetrySnapshot& snapshot,
    const std::string& siteId,
    const std::string& observedAtIso8601);

} // namespace ring_iot

