#include "DeviceConfig.h"
#include "Device.h"
#include "Diagnostics.h"
#include "HealthMonitor.h"
#include "MqttPublisher.h"
#include "MqttTopics.h"
#include "RecoveryManager.h"
#include "TelemetryManager.h"
#include "TelemetrySerializer.h"
#include "Watchdog.h"

#include <chrono>
#include <iostream>
#include <memory>
#include <thread>

int main(int argc, char* argv[]) {
    std::string configPath = "device_simulator/config/device_config.example.json";
    bool mqttEnabled = false;

    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--mqtt") {
            mqttEnabled = true;
        } else {
            configPath = argument;
        }
    }

    const auto config = ring_iot::loadDeviceConfig(configPath);
    const auto topics = ring_iot::buildMqttTopics(config.mqttBaseTopic);

    ring_iot::Device device(config.deviceId);
    ring_iot::TelemetryProfile profile;
    profile.baselineCpuPercent = config.baselineCpuPercent;
    profile.baselineMemoryPercent = config.baselineMemoryPercent;
    profile.baselineTemperatureCelsius = config.baselineTemperatureCelsius;

    ring_iot::TelemetryManager telemetry(device.id(), profile);
    ring_iot::HealthMonitor healthMonitor;
    ring_iot::RecoveryManager recoveryManager;
    ring_iot::Watchdog watchdog(std::chrono::duration_cast<std::chrono::seconds>(config.watchdogTimeout));
    std::unique_ptr<ring_iot::MqttPublisher> mqttPublisher;

    device.boot();
    watchdog.markHeartbeat();

    std::cout << "Device simulator skeleton initialized for " << device.id() << '\n';

    if (mqttEnabled) {
        mqttPublisher = std::make_unique<ring_iot::MqttPublisher>(
            config.mqttBrokerHost,
            static_cast<std::uint16_t>(config.mqttBrokerPort),
            "device-simulator-" + config.deviceId);

        if (!mqttPublisher->connect()) {
            std::cerr << "MQTT connection failed: " << mqttPublisher->lastError() << '\n';
            return 2;
        }

        std::cout << "MQTT publisher connected to " << config.mqttBrokerHost << ":"
                  << config.mqttBrokerPort << '\n';
    }

    for (int sampleIndex = 0; sampleIndex < config.sampleCount; ++sampleIndex) {
        const auto snapshot = telemetry.collectSnapshot();
        const auto health = healthMonitor.evaluate(snapshot);
        const auto action = recoveryManager.recommendAction(health);
        recoveryManager.recordAttempt(action);
        watchdog.markHeartbeat();

        const auto telemetryPayload = serializeTelemetryJson(snapshot, config.siteId, "2026-05-28T17:00:00Z");
        std::cout << telemetryPayload << '\n';
        if (mqttPublisher && !mqttPublisher->publish(topics.telemetry, telemetryPayload)) {
            std::cerr << "MQTT telemetry publish failed: " << mqttPublisher->lastError() << '\n';
            return 3;
        }

        if (health != ring_iot::HealthState::Healthy) {
            const ring_iot::DiagnosticsEvent event{
                snapshot.deviceId,
                health,
                ring_iot::classifyReasonCode(snapshot),
                action};
            const auto diagnosticsPayload = serializeDiagnosticsJson(event, "2026-05-28T17:00:00Z");
            std::cout << diagnosticsPayload << '\n';
            if (mqttPublisher && !mqttPublisher->publish(topics.diagnostics, diagnosticsPayload)) {
                std::cerr << "MQTT diagnostics publish failed: " << mqttPublisher->lastError() << '\n';
                return 4;
            }
        }

        if (sampleIndex + 1 < config.sampleCount) {
            std::this_thread::sleep_for(config.telemetryInterval);
        }
    }

    device.shutdown();
    if (mqttPublisher) {
        mqttPublisher->disconnect();
    }

    return 0;
}
