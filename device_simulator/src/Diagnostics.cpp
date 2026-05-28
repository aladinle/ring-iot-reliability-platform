#include "Diagnostics.h"

#include <sstream>

namespace ring_iot {

ReasonCode classifyReasonCode(const TelemetrySnapshot& snapshot) {
    if (snapshot.temperatureCelsius >= 85.0) {
        return ReasonCode::ThermalPressure;
    }

    if (snapshot.memoryPercent >= 80.0) {
        return ReasonCode::MemoryPressure;
    }

    if (snapshot.cpuPercent >= 80.0) {
        return ReasonCode::HighCpu;
    }

    return ReasonCode::Normal;
}

const char* toString(HealthState state) {
    switch (state) {
    case HealthState::Healthy:
        return "healthy";
    case HealthState::Degraded:
        return "degraded";
    case HealthState::Critical:
        return "critical";
    }

    return "unknown";
}

const char* toString(ReasonCode reasonCode) {
    switch (reasonCode) {
    case ReasonCode::Normal:
        return "normal";
    case ReasonCode::HighCpu:
        return "high_cpu";
    case ReasonCode::MemoryPressure:
        return "memory_pressure";
    case ReasonCode::ThermalPressure:
        return "thermal_pressure";
    }

    return "unknown";
}

const char* toString(RecoveryAction action) {
    switch (action) {
    case RecoveryAction::None:
        return "none";
    case RecoveryAction::RestartService:
        return "restart_service";
    case RecoveryAction::ResetNetwork:
        return "reset_network";
    case RecoveryAction::EnterSafeMode:
        return "enter_safe_mode";
    }

    return "unknown";
}

std::string serializeDiagnosticsJson(
    const DiagnosticsEvent& event,
    const std::string& observedAtIso8601) {
    std::ostringstream output;
    output << "{";
    output << "\"schema_version\":\"1.0\",";
    output << "\"device_id\":\"" << event.deviceId << "\",";
    output << "\"event_type\":\"diagnostics\",";
    output << "\"health_state\":\"" << toString(event.healthState) << "\",";
    output << "\"severity\":\"" << (event.healthState == HealthState::Critical ? "critical" : "warning") << "\",";
    output << "\"reason_code\":\"" << toString(event.reasonCode) << "\",";
    output << "\"recommended_action\":\"" << toString(event.recommendedAction) << "\",";
    output << "\"observed_at\":\"" << observedAtIso8601 << "\"";
    output << "}";
    return output.str();
}

} // namespace ring_iot

