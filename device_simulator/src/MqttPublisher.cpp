#include "MqttPublisher.h"

#include <cstring>
#include <utility>
#include <vector>

#ifdef _WIN32
#define NOMINMAX
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>
#endif

namespace ring_iot {

namespace {

void appendString(std::vector<unsigned char>& packet, const std::string& value) {
    packet.push_back(static_cast<unsigned char>((value.size() >> 8) & 0xFF));
    packet.push_back(static_cast<unsigned char>(value.size() & 0xFF));
    packet.insert(packet.end(), value.begin(), value.end());
}

void appendRemainingLength(std::vector<unsigned char>& packet, std::size_t length) {
    do {
        unsigned char encoded = static_cast<unsigned char>(length % 128);
        length /= 128;
        if (length > 0) {
            encoded |= 128;
        }
        packet.push_back(encoded);
    } while (length > 0);
}

std::vector<unsigned char> buildConnectPacket(const std::string& clientId) {
    std::vector<unsigned char> variable;
    appendString(variable, "MQTT");
    variable.push_back(0x04);
    variable.push_back(0x02);
    variable.push_back(0x00);
    variable.push_back(0x3C);
    appendString(variable, clientId);

    std::vector<unsigned char> packet;
    packet.push_back(0x10);
    appendRemainingLength(packet, variable.size());
    packet.insert(packet.end(), variable.begin(), variable.end());
    return packet;
}

std::vector<unsigned char> buildPublishPacket(const std::string& topic, const std::string& payload) {
    std::vector<unsigned char> variable;
    appendString(variable, topic);
    variable.insert(variable.end(), payload.begin(), payload.end());

    std::vector<unsigned char> packet;
    packet.push_back(0x30);
    appendRemainingLength(packet, variable.size());
    packet.insert(packet.end(), variable.begin(), variable.end());
    return packet;
}

#ifdef _WIN32
using SocketType = SOCKET;
constexpr SocketType invalidSocket = INVALID_SOCKET;
#else
using SocketType = int;
constexpr SocketType invalidSocket = -1;
#endif

} // namespace

MqttPublisher::MqttPublisher(std::string host, std::uint16_t port, std::string clientId)
    : host_(std::move(host)), port_(port), clientId_(std::move(clientId)) {}

MqttPublisher::~MqttPublisher() {
    disconnect();
}

bool MqttPublisher::connect() {
#ifdef _WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        lastError_ = "WSAStartup failed";
        return false;
    }
#endif

    addrinfo hints{};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    addrinfo* result = nullptr;
    const auto portText = std::to_string(port_);
    if (getaddrinfo(host_.c_str(), portText.c_str(), &hints, &result) != 0) {
        lastError_ = "could not resolve MQTT broker host";
        return false;
    }

    SocketType socketValue = invalidSocket;
    for (addrinfo* ptr = result; ptr != nullptr; ptr = ptr->ai_next) {
        socketValue = ::socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
        if (socketValue == invalidSocket) {
            continue;
        }

        if (::connect(socketValue, ptr->ai_addr, static_cast<int>(ptr->ai_addrlen)) == 0) {
            break;
        }

#ifdef _WIN32
        closesocket(socketValue);
#else
        close(socketValue);
#endif
        socketValue = invalidSocket;
    }
    freeaddrinfo(result);

    if (socketValue == invalidSocket) {
        lastError_ = "could not connect to MQTT broker";
        return false;
    }

    socketHandle_ = static_cast<decltype(socketHandle_)>(socketValue);
    const auto packet = buildConnectPacket(clientId_);
    if (!sendAll(packet.data(), static_cast<int>(packet.size()))) {
        return false;
    }

    unsigned char response[4]{};
    const int received = recv(static_cast<SocketType>(socketHandle_), reinterpret_cast<char*>(response), 4, 0);
    if (received < 4 || response[0] != 0x20 || response[3] != 0x00) {
        lastError_ = "MQTT broker rejected connection";
        disconnect();
        return false;
    }

    connected_ = true;
    return true;
}

bool MqttPublisher::publish(const std::string& topic, const std::string& payload) {
    if (!connected_) {
        lastError_ = "MQTT publisher is not connected";
        return false;
    }

    const auto packet = buildPublishPacket(topic, payload);
    return sendAll(packet.data(), static_cast<int>(packet.size()));
}

void MqttPublisher::disconnect() {
    if (socketHandle_ != 0
#ifndef _WIN32
        && socketHandle_ != -1
#endif
    ) {
        const unsigned char disconnectPacket[] = {0xE0, 0x00};
        sendAll(disconnectPacket, 2);
#ifdef _WIN32
        closesocket(static_cast<SocketType>(socketHandle_));
        WSACleanup();
        socketHandle_ = 0;
#else
        close(socketHandle_);
        socketHandle_ = -1;
#endif
    }
    connected_ = false;
}

const std::string& MqttPublisher::lastError() const {
    return lastError_;
}

bool MqttPublisher::sendAll(const unsigned char* data, int length) {
    int totalSent = 0;
    while (totalSent < length) {
        const int sent = send(
            static_cast<SocketType>(socketHandle_),
            reinterpret_cast<const char*>(data + totalSent),
            length - totalSent,
            0);
        if (sent <= 0) {
            lastError_ = "socket send failed";
            return false;
        }
        totalSent += sent;
    }
    return true;
}

} // namespace ring_iot
