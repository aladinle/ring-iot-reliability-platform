#include "DeviceConfig.h"
#include "Device.h"
#include "Diagnostics.h"
#include "HealthMonitor.h"
#include "MqttTopics.h"
#include "RecoveryManager.h"
#include "TelemetrySerializer.h"

#include <cassert>

int main() {
    ring_iot::Device device("test-device");
    assert(device.state() == ring_iot::DeviceState::Offline);

    device.boot();
    assert(device.state() == ring_iot::DeviceState::Healthy);

    ring_iot::TelemetrySnapshot snapshot;
    snapshot.cpuPercent = 96.0;

    ring_iot::HealthMonitor healthMonitor;
    assert(healthMonitor.evaluate(snapshot) == ring_iot::HealthState::Critical);
    assert(ring_iot::classifyReasonCode(snapshot) == ring_iot::ReasonCode::HighCpu);

    ring_iot::TelemetrySnapshot degradedSnapshot;
    degradedSnapshot.cpuPercent = 81.0;
    degradedSnapshot.memoryPercent = 45.0;
    degradedSnapshot.temperatureCelsius = 40.0;
    assert(healthMonitor.evaluate(degradedSnapshot) == ring_iot::HealthState::Degraded);
    assert(ring_iot::classifyReasonCode(degradedSnapshot) == ring_iot::ReasonCode::HighCpu);

    ring_iot::TelemetrySnapshot memorySnapshot;
    memorySnapshot.cpuPercent = 30.0;
    memorySnapshot.memoryPercent = 85.0;
    assert(ring_iot::classifyReasonCode(memorySnapshot) == ring_iot::ReasonCode::MemoryPressure);

    ring_iot::TelemetrySnapshot thermalSnapshot;
    thermalSnapshot.temperatureCelsius = 86.0;
    assert(healthMonitor.evaluate(thermalSnapshot) == ring_iot::HealthState::Critical);
    assert(ring_iot::classifyReasonCode(thermalSnapshot) == ring_iot::ReasonCode::ThermalPressure);

    ring_iot::TelemetryProfile profile;
    profile.baselineCpuPercent = 22.0;
    profile.baselineMemoryPercent = 33.0;
    profile.baselineTemperatureCelsius = 44.0;

    ring_iot::TelemetryManager telemetry(device.id(), profile);
    const auto collected = telemetry.collectSnapshot();
    assert(collected.deviceId == "test-device");
    assert(collected.cpuPercent == 22.0);
    assert(collected.memoryPercent == 33.0);
    assert(collected.temperatureCelsius == 44.0);

    const auto config = ring_iot::loadDeviceConfig("tests/fixtures/device_config.test.json");
    assert(config.deviceId == "ring-test-001");
    assert(config.siteId == "test-lab");
    assert(config.telemetryInterval.count() == 250);
    assert(config.watchdogTimeout.count() == 5000);
    assert(config.sampleCount == 2);
    assert(config.baselineCpuPercent == 11.5);
    assert(config.baselineMemoryPercent == 22.5);
    assert(config.baselineTemperatureCelsius == 33.5);
    assert(config.mqttBrokerHost == "localhost");
    assert(config.mqttBrokerPort == 1883);
    assert(config.mqttBaseTopic == "devices/ring-test-001");

    const auto topics = ring_iot::buildMqttTopics(config.mqttBaseTopic);
    assert(topics.telemetry == "devices/ring-test-001/telemetry");
    assert(topics.diagnostics == "devices/ring-test-001/diagnostics");
    assert(topics.heartbeat == "devices/ring-test-001/heartbeat");
    assert(topics.recovery == "devices/ring-test-001/recovery");

    const auto payload = ring_iot::serializeTelemetryJson(collected, "test-lab", "2026-05-28T17:00:00Z");
    assert(payload.find("\"schema_version\":\"1.0\"") != std::string::npos);
    assert(payload.find("\"device_id\":\"test-device\"") != std::string::npos);
    assert(payload.find("\"site_id\":\"test-lab\"") != std::string::npos);
    assert(payload.find("\"cpu_percent\":22") != std::string::npos);

    ring_iot::RecoveryManager recoveryManager(2);
    assert(recoveryManager.recommendAction(ring_iot::HealthState::Critical) ==
           ring_iot::RecoveryAction::RestartService);
    assert(recoveryManager.recommendAction(ring_iot::HealthState::Degraded) ==
           ring_iot::RecoveryAction::ResetNetwork);
    assert(ring_iot::toString(ring_iot::RecoveryAction::RestartService) == std::string("restart_service"));

    const auto firstRecovery = recoveryManager.recordAttempt(
        "test-device",
        ring_iot::RecoveryAction::RestartService,
        "high_cpu");
    assert(firstRecovery.result == ring_iot::RecoveryResult::Started);
    assert(firstRecovery.attempt == 1);
    assert(recoveryManager.attempts() == 1);

    const auto recoveryPayload = ring_iot::serializeRecoveryJson(firstRecovery, "2026-05-28T17:00:00Z");
    assert(recoveryPayload.find("\"event_type\":\"recovery\"") != std::string::npos);
    assert(recoveryPayload.find("\"action\":\"restart_service\"") != std::string::npos);
    assert(recoveryPayload.find("\"result\":\"started\"") != std::string::npos);

    const ring_iot::DiagnosticsEvent event{
        "test-device",
        ring_iot::HealthState::Critical,
        ring_iot::ReasonCode::HighCpu,
        ring_iot::RecoveryAction::RestartService,
        ring_iot::Severity::Critical};
    const auto diagnosticsPayload = ring_iot::serializeDiagnosticsJson(event, "2026-05-28T17:00:00Z");
    assert(diagnosticsPayload.find("\"event_type\":\"diagnostics\"") != std::string::npos);
    assert(diagnosticsPayload.find("\"health_state\":\"critical\"") != std::string::npos);
    assert(diagnosticsPayload.find("\"reason_code\":\"high_cpu\"") != std::string::npos);
    assert(diagnosticsPayload.find("\"recommended_action\":\"restart_service\"") != std::string::npos);

    const ring_iot::DiagnosticsEngine diagnosticsEngine;
    const auto evaluatedEvent = diagnosticsEngine.evaluate(
        degradedSnapshot,
        ring_iot::HealthState::Degraded,
        ring_iot::RecoveryAction::ResetNetwork);
    assert(evaluatedEvent.severity == ring_iot::Severity::Warning);
    assert(evaluatedEvent.reasonCode == ring_iot::ReasonCode::HighCpu);

    device.shutdown();
    assert(device.state() == ring_iot::DeviceState::Offline);

    return 0;
}
