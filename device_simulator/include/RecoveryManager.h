#pragma once

#include "HealthMonitor.h"

namespace ring_iot {

enum class RecoveryAction {
    None,
    RestartService,
    ResetNetwork,
    EnterSafeMode
};

class RecoveryManager {
public:
    RecoveryAction recommendAction(HealthState state) const;
    void recordAttempt(RecoveryAction action);
};

} // namespace ring_iot

