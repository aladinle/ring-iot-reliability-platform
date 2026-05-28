#include "MqttTopics.h"

namespace ring_iot {

MqttTopics buildMqttTopics(const std::string& baseTopic) {
    return MqttTopics{
        baseTopic + "/telemetry",
        baseTopic + "/diagnostics",
        baseTopic + "/heartbeat",
        baseTopic + "/recovery"};
}

} // namespace ring_iot

