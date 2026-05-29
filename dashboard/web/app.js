const mockSnapshot = {
  fleet_health: {
    healthy: 1,
    degraded: 1,
    critical: 1
  },
  devices: [
    {
      device_id: "ring-sim-healthy",
      health_state: "healthy",
      cpu_percent: 24,
      memory_percent: 48,
      temperature_celsius: 39.5,
      uptime_seconds: 120
    },
    {
      device_id: "ring-sim-degraded",
      health_state: "degraded",
      cpu_percent: 84,
      memory_percent: 61,
      temperature_celsius: 52,
      uptime_seconds: 180
    },
    {
      device_id: "ring-sim-critical",
      health_state: "critical",
      cpu_percent: 97,
      memory_percent: 88,
      temperature_celsius: 72,
      uptime_seconds: 240
    }
  ],
  alerts: [
    {
      device_id: "ring-sim-degraded",
      severity: "warning",
      reason_code: "high_cpu",
      recommended_action: "reset_network"
    },
    {
      device_id: "ring-sim-critical",
      severity: "critical",
      reason_code: "memory_pressure",
      recommended_action: "restart_service"
    }
  ],
  recoveries: [
    {
      device_id: "ring-sim-degraded",
      action: "reset_network",
      result: "started",
      attempt: 1
    },
    {
      device_id: "ring-sim-critical",
      action: "restart_service",
      result: "started",
      attempt: 1
    }
  ]
};

function byId(id) {
  return document.getElementById(id);
}

function renderSnapshot(snapshot) {
  const fleet = snapshot.fleet_health || summarizeFleet(snapshot.devices || []);
  byId("healthyCount").textContent = fleet.healthy || 0;
  byId("degradedCount").textContent = fleet.degraded || 0;
  byId("criticalCount").textContent = fleet.critical || 0;

  const devices = snapshot.devices || [];
  byId("deviceCount").textContent = `${devices.length} devices`;
  byId("deviceRows").innerHTML = devices.map(renderDeviceRow).join("");

  const alerts = snapshot.alerts || [];
  byId("alertCount").textContent = `${alerts.length} alerts`;
  byId("alertList").innerHTML = alerts.length
    ? alerts.map(renderAlert).join("")
    : `<div class="event"><strong>No active diagnostics</strong><p>Fleet is currently healthy.</p></div>`;

  const recoveries = snapshot.recoveries || [];
  byId("recoveryCount").textContent = `${recoveries.length} events`;
  byId("recoveryList").innerHTML = recoveries.length
    ? recoveries.map(renderRecovery).join("")
    : `<div class="event"><strong>No recovery activity</strong><p>No automated recovery actions recorded.</p></div>`;
}

function renderDeviceRow(device) {
  return `
    <tr>
      <td>${escapeHtml(device.device_id)}</td>
      <td><span class="badge ${escapeHtml(device.health_state)}">${escapeHtml(device.health_state)}</span></td>
      <td>${Number(device.cpu_percent).toFixed(1)}%</td>
      <td>${Number(device.memory_percent).toFixed(1)}%</td>
      <td>${Number(device.temperature_celsius).toFixed(1)}C</td>
      <td>${Number(device.uptime_seconds)}s</td>
    </tr>
  `;
}

function renderAlert(alert) {
  return `
    <div class="event">
      <strong>${escapeHtml(alert.device_id)} · ${escapeHtml(alert.severity)}</strong>
      <p>Reason: ${escapeHtml(alert.reason_code)}<br>Recommended action: ${escapeHtml(alert.recommended_action)}</p>
    </div>
  `;
}

function renderRecovery(recovery) {
  return `
    <div class="event">
      <strong>${escapeHtml(recovery.device_id)} · ${escapeHtml(recovery.action)}</strong>
      <p>Result: ${escapeHtml(recovery.result)}<br>Attempt: ${Number(recovery.attempt)}</p>
    </div>
  `;
}

function summarizeFleet(devices) {
  return devices.reduce(
    (summary, device) => {
      if (Object.prototype.hasOwnProperty.call(summary, device.health_state)) {
        summary[device.health_state] += 1;
      }
      return summary;
    },
    { healthy: 0, degraded: 0, critical: 0 }
  );
}

async function refreshBackendHealth() {
  try {
    const response = await fetch("http://127.0.0.1:8080/health");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const payload = await response.json();
    byId("backendStatus").textContent = `Backend status: ${payload.status}`;
  } catch (error) {
    byId("backendStatus").textContent = "Backend status: unavailable, using mock fleet";
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

byId("refreshButton").addEventListener("click", refreshBackendHealth);
byId("mockButton").addEventListener("click", () => renderSnapshot(mockSnapshot));

renderSnapshot(mockSnapshot);
refreshBackendHealth();

