#include "RecoveryManager.h"

#include <sstream>

namespace ring_iot {

RecoveryManager::RecoveryManager(int maxAttempts)
    : maxAttempts_(maxAttempts) {}

RecoveryAction RecoveryManager::recommendAction(HealthState state) const {
    if (attempts_ >= maxAttempts_) {
        return RecoveryAction::EnterSafeMode;
    }

    if (state == HealthState::Critical) {
        return RecoveryAction::RestartService;
    }

    if (state == HealthState::Degraded) {
        return RecoveryAction::ResetNetwork;
    }

    return RecoveryAction::None;
}

RecoveryEvent RecoveryManager::recordAttempt(
    const std::string& deviceId,
    RecoveryAction action,
    const std::string& reasonCode) {
    if (action == RecoveryAction::None) {
        return RecoveryEvent{deviceId, action, RecoveryResult::Skipped, attempts_, reasonCode};
    }

    if (attempts_ >= maxAttempts_ && action != RecoveryAction::EnterSafeMode) {
        return RecoveryEvent{deviceId, action, RecoveryResult::Suppressed, attempts_, reasonCode};
    }

    ++attempts_;
    return RecoveryEvent{deviceId, action, RecoveryResult::Started, attempts_, reasonCode};
}

int RecoveryManager::attempts() const {
    return attempts_;
}

const char* toString(RecoveryResult result) {
    switch (result) {
    case RecoveryResult::Skipped:
        return "skipped";
    case RecoveryResult::Started:
        return "started";
    case RecoveryResult::Suppressed:
        return "suppressed";
    }

    return "unknown";
}

std::string serializeRecoveryJson(
    const RecoveryEvent& event,
    const std::string& observedAtIso8601) {
    auto actionText = "none";
    switch (event.action) {
    case RecoveryAction::None:
        actionText = "none";
        break;
    case RecoveryAction::RestartService:
        actionText = "restart_service";
        break;
    case RecoveryAction::ResetNetwork:
        actionText = "reset_network";
        break;
    case RecoveryAction::EnterSafeMode:
        actionText = "enter_safe_mode";
        break;
    }

    std::ostringstream output;
    output << "{";
    output << "\"schema_version\":\"1.0\",";
    output << "\"device_id\":\"" << event.deviceId << "\",";
    output << "\"event_type\":\"recovery\",";
    output << "\"action\":\"" << actionText << "\",";
    output << "\"result\":\"" << toString(event.result) << "\",";
    output << "\"attempt\":" << event.attempt << ",";
    output << "\"reason_code\":\"" << event.reasonCode << "\",";
    output << "\"observed_at\":\"" << observedAtIso8601 << "\"";
    output << "}";
    return output.str();
}

} // namespace ring_iot
