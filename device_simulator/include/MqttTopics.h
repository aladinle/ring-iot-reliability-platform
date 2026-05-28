#pragma once

#include <string>

namespace ring_iot {

struct MqttTopics {
    std::string telemetry;
    std::string diagnostics;
    std::string heartbeat;
    std::string recovery;
};

MqttTopics buildMqttTopics(const std::string& baseTopic);

} // namespace ring_iot

