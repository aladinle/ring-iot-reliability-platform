#pragma once

#include <chrono>

namespace ring_iot {

class Watchdog {
public:
    explicit Watchdog(std::chrono::seconds timeout);

    void markHeartbeat();
    bool hasTimedOut() const;

private:
    std::chrono::seconds timeout_;
    std::chrono::steady_clock::time_point lastHeartbeat_;
};

} // namespace ring_iot

