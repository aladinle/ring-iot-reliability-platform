#pragma once

#include <string>

namespace ring_iot {

enum class DeviceState {
    Offline,
    Booting,
    Healthy,
    Degraded,
    Recovering
};

class Device {
public:
    explicit Device(std::string deviceId);

    const std::string& id() const;
    DeviceState state() const;

    void boot();
    void shutdown();

private:
    std::string deviceId_;
    DeviceState state_;
};

} // namespace ring_iot

