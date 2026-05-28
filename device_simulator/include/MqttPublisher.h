#pragma once

#include <cstdint>
#include <string>

namespace ring_iot {

class MqttPublisher {
public:
    MqttPublisher(std::string host, std::uint16_t port, std::string clientId);
    ~MqttPublisher();

    MqttPublisher(const MqttPublisher&) = delete;
    MqttPublisher& operator=(const MqttPublisher&) = delete;

    bool connect();
    bool publish(const std::string& topic, const std::string& payload);
    void disconnect();
    const std::string& lastError() const;

private:
    std::string host_;
    std::uint16_t port_;
    std::string clientId_;
    std::string lastError_;
    bool connected_ = false;

#ifdef _WIN32
    std::uintptr_t socketHandle_ = 0;
#else
    int socketHandle_ = -1;
#endif

    bool sendAll(const unsigned char* data, int length);
};

} // namespace ring_iot

