#pragma once

#include <chrono>
#include <string>

namespace ring_iot {

struct DeviceConfig {
    std::string deviceId = "ring-sim-001";
    std::string siteId = "lab-001";
    std::chrono::milliseconds telemetryInterval{1000};
    std::chrono::milliseconds watchdogTimeout{30000};
    int sampleCount = 1;
    double baselineCpuPercent = 24.0;
    double baselineMemoryPercent = 48.0;
    double baselineTemperatureCelsius = 39.5;
    std::string mqttBrokerHost = "localhost";
    int mqttBrokerPort = 1883;
    std::string mqttBaseTopic = "devices/ring-sim-001";
};

DeviceConfig loadDeviceConfig(const std::string& path);

} // namespace ring_iot
