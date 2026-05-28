#include "TelemetrySerializer.h"

#include <sstream>

namespace ring_iot {

std::string serializeTelemetryJson(
    const TelemetrySnapshot& snapshot,
    const std::string& siteId,
    const std::string& observedAtIso8601) {
    std::ostringstream output;
    output << "{";
    output << "\"schema_version\":\"1.0\",";
    output << "\"device_id\":\"" << snapshot.deviceId << "\",";
    output << "\"site_id\":\"" << siteId << "\",";
    output << "\"observed_at\":\"" << observedAtIso8601 << "\",";
    output << "\"metrics\":{";
    output << "\"cpu_percent\":" << snapshot.cpuPercent << ",";
    output << "\"memory_percent\":" << snapshot.memoryPercent << ",";
    output << "\"temperature_celsius\":" << snapshot.temperatureCelsius << ",";
    output << "\"uptime_seconds\":" << snapshot.uptime.count();
    output << "}";
    output << "}";
    return output.str();
}

} // namespace ring_iot

