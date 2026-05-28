#include "DeviceConfig.h"

#include <fstream>
#include <regex>
#include <sstream>

namespace ring_iot {

namespace {

std::string readFile(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        return {};
    }

    std::ostringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

std::string findString(const std::string& content, const std::string& key, const std::string& fallback) {
    const std::regex pattern("\"" + key + "\"\\s*:\\s*\"([^\"]+)\"");
    std::smatch match;
    if (std::regex_search(content, match, pattern)) {
        return match[1].str();
    }
    return fallback;
}

int findInt(const std::string& content, const std::string& key, int fallback) {
    const std::regex pattern("\"" + key + "\"\\s*:\\s*([0-9]+)");
    std::smatch match;
    if (std::regex_search(content, match, pattern)) {
        return std::stoi(match[1].str());
    }
    return fallback;
}

double findDouble(const std::string& content, const std::string& key, double fallback) {
    const std::regex pattern("\"" + key + "\"\\s*:\\s*([0-9]+(?:\\.[0-9]+)?)");
    std::smatch match;
    if (std::regex_search(content, match, pattern)) {
        return std::stod(match[1].str());
    }
    return fallback;
}

} // namespace

DeviceConfig loadDeviceConfig(const std::string& path) {
    DeviceConfig config;
    const auto content = readFile(path);
    if (content.empty()) {
        return config;
    }

    config.deviceId = findString(content, "device_id", config.deviceId);
    config.siteId = findString(content, "site_id", config.siteId);
    config.telemetryInterval = std::chrono::milliseconds(
        findInt(content, "telemetry_interval_ms", static_cast<int>(config.telemetryInterval.count())));
    config.watchdogTimeout = std::chrono::milliseconds(
        findInt(content, "watchdog_timeout_ms", static_cast<int>(config.watchdogTimeout.count())));
    config.sampleCount = findInt(content, "sample_count", config.sampleCount);
    if (config.sampleCount < 1) {
        config.sampleCount = 1;
    }

    // Optional simulator-only baseline fields can be added to config without changing the schema contract.
    config.baselineCpuPercent = findDouble(content, "baseline_cpu_percent", config.baselineCpuPercent);
    config.baselineMemoryPercent = findDouble(content, "baseline_memory_percent", config.baselineMemoryPercent);
    config.baselineTemperatureCelsius =
        findDouble(content, "baseline_temperature_celsius", config.baselineTemperatureCelsius);
    config.mqttBrokerHost = findString(content, "broker_host", config.mqttBrokerHost);
    config.mqttBrokerPort = findInt(content, "broker_port", config.mqttBrokerPort);
    config.mqttBaseTopic = findString(content, "base_topic", "devices/" + config.deviceId);

    return config;
}

} // namespace ring_iot
