#include "Device.h"

#include <utility>

namespace ring_iot {

Device::Device(std::string deviceId)
    : deviceId_(std::move(deviceId)), state_(DeviceState::Offline) {}

const std::string& Device::id() const {
    return deviceId_;
}

DeviceState Device::state() const {
    return state_;
}

void Device::boot() {
    // Future implementation: load config, initialize services, and start worker threads.
    state_ = DeviceState::Healthy;
}

void Device::shutdown() {
    // Future implementation: coordinate thread shutdown and flush final diagnostics.
    state_ = DeviceState::Offline;
}

} // namespace ring_iot

