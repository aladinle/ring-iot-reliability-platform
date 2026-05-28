#pragma once

#include "HealthMonitor.h"

#include <string>

namespace ring_iot {

enum class RecoveryAction {
    None,
    RestartService,
    ResetNetwork,
    EnterSafeMode
};

enum class RecoveryResult {
    Skipped,
    Started,
    Suppressed
};

struct RecoveryEvent {
    std::string deviceId;
    RecoveryAction action = RecoveryAction::None;
    RecoveryResult result = RecoveryResult::Skipped;
    int attempt = 0;
    std::string reasonCode = "normal";
};

class RecoveryManager {
public:
    explicit RecoveryManager(int maxAttempts = 3);

    RecoveryAction recommendAction(HealthState state) const;
    RecoveryEvent recordAttempt(
        const std::string& deviceId,
        RecoveryAction action,
        const std::string& reasonCode);
    int attempts() const;

private:
    int maxAttempts_;
    int attempts_ = 0;
};

const char* toString(RecoveryResult result);
std::string serializeRecoveryJson(
    const RecoveryEvent& event,
    const std::string& observedAtIso8601);

} // namespace ring_iot
