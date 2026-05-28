#pragma once

#include "HealthMonitor.h"
#include "RecoveryManager.h"
#include "TelemetryManager.h"

#include <string>

namespace ring_iot {

enum class ReasonCode {
    Normal,
    HighCpu,
    MemoryPressure,
    ThermalPressure,
    HeartbeatTimeout,
    TelemetryStale,
    RepeatedRecovery
};

enum class Severity {
    Info,
    Warning,
    Critical
};

struct DiagnosticsEvent {
    std::string deviceId;
    HealthState healthState = HealthState::Healthy;
    ReasonCode reasonCode = ReasonCode::Normal;
    RecoveryAction recommendedAction = RecoveryAction::None;
    Severity severity = Severity::Info;
};

ReasonCode classifyReasonCode(const TelemetrySnapshot& snapshot);
Severity severityForHealth(HealthState state);
const char* toString(HealthState state);
const char* toString(Severity severity);
const char* toString(ReasonCode reasonCode);
const char* toString(RecoveryAction action);
std::string serializeDiagnosticsJson(
    const DiagnosticsEvent& event,
    const std::string& observedAtIso8601);

class DiagnosticsEngine {
public:
    DiagnosticsEvent evaluate(
        const TelemetrySnapshot& snapshot,
        HealthState healthState,
        RecoveryAction recommendedAction) const;
};

} // namespace ring_iot
