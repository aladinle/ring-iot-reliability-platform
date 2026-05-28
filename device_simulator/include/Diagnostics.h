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
    ThermalPressure
};

struct DiagnosticsEvent {
    std::string deviceId;
    HealthState healthState = HealthState::Healthy;
    ReasonCode reasonCode = ReasonCode::Normal;
    RecoveryAction recommendedAction = RecoveryAction::None;
};

ReasonCode classifyReasonCode(const TelemetrySnapshot& snapshot);
const char* toString(HealthState state);
const char* toString(ReasonCode reasonCode);
const char* toString(RecoveryAction action);
std::string serializeDiagnosticsJson(
    const DiagnosticsEvent& event,
    const std::string& observedAtIso8601);

} // namespace ring_iot

