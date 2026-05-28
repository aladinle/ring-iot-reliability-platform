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
    case ReasonCode::HeartbeatTimeout:
        return "heartbeat_timeout";
    case ReasonCode::TelemetryStale:
        return "telemetry_stale";
    case ReasonCode::RepeatedRecovery:
        return "repeated_recovery";
    }

    return "unknown";
}

Severity severityForHealth(HealthState state) {
    switch (state) {
    case HealthState::Healthy:
        return Severity::Info;
    case HealthState::Degraded:
        return Severity::Warning;
    case HealthState::Critical:
        return Severity::Critical;
    }

    return Severity::Info;
}

const char* toString(Severity severity) {
    switch (severity) {
    case Severity::Info:
        return "info";
    case Severity::Warning:
        return "warning";
    case Severity::Critical:
        return "critical";
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
    output << "\"severity\":\"" << toString(event.severity) << "\",";
    output << "\"reason_code\":\"" << toString(event.reasonCode) << "\",";
    output << "\"recommended_action\":\"" << toString(event.recommendedAction) << "\",";
    output << "\"observed_at\":\"" << observedAtIso8601 << "\"";
    output << "}";
    return output.str();
}

DiagnosticsEvent DiagnosticsEngine::evaluate(
    const TelemetrySnapshot& snapshot,
    HealthState healthState,
    RecoveryAction recommendedAction) const {
    return DiagnosticsEvent{
        snapshot.deviceId,
        healthState,
        classifyReasonCode(snapshot),
        recommendedAction,
        severityForHealth(healthState)};
}

} // namespace ring_iot
