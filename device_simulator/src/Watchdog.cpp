#include "Watchdog.h"

namespace ring_iot {

Watchdog::Watchdog(std::chrono::seconds timeout)
    : timeout_(timeout), lastHeartbeat_(std::chrono::steady_clock::now()) {}

void Watchdog::markHeartbeat() {
    lastHeartbeat_ = std::chrono::steady_clock::now();
}

bool Watchdog::hasTimedOut() const {
    // Future implementation: emit diagnostic context when timeout threshold is crossed.
    return (std::chrono::steady_clock::now() - lastHeartbeat_) > timeout_;
}

} // namespace ring_iot

