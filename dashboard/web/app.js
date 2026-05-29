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
  ],
  anomalies: [
    {
      device_id: "ring-sim-critical",
      score: 0.97,
      reason: "critical_resource_pressure",
      severity: "critical",
      is_anomaly: true
    }
  ]
};

const sessionKey = "ring_iot_session";
let autoRefreshTimer = null;

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

  const anomalies = snapshot.anomalies || [];
  byId("anomalyCount").textContent = `${anomalies.length} scores`;
  byId("anomalyList").innerHTML = anomalies.length
    ? anomalies.map(renderAnomaly).join("")
    : `<div class="event"><strong>No anomaly scores</strong><p>No AI inference results recorded yet.</p></div>`;
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
      <strong>${escapeHtml(alert.device_id)} - ${escapeHtml(alert.severity)}</strong>
      <p>Reason: ${escapeHtml(alert.reason_code)}<br>Recommended action: ${escapeHtml(alert.recommended_action)}</p>
    </div>
  `;
}

function renderRecovery(recovery) {
  return `
    <div class="event">
      <strong>${escapeHtml(recovery.device_id)} - ${escapeHtml(recovery.action)}</strong>
      <p>Result: ${escapeHtml(recovery.result)}<br>Attempt: ${Number(recovery.attempt)}</p>
    </div>
  `;
}

function renderAnomaly(anomaly) {
  return `
    <div class="event">
      <strong>${escapeHtml(anomaly.device_id)} - ${escapeHtml(anomaly.severity)}</strong>
      <p>Score: ${Number(anomaly.score).toFixed(2)}<br>Reason: ${escapeHtml(anomaly.reason)}</p>
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
    await refreshDashboardSnapshot();
  } catch (error) {
    byId("backendStatus").textContent = "Backend status: unavailable, using mock fleet";
  }
}

async function refreshDashboardSnapshot() {
  const session = getSession();
  if (!session) {
    byId("sessionStatus").textContent = "Session: signed out, login to load backend dashboard";
    return;
  }

  const response = await fetch("http://127.0.0.1:8080/api/dashboard/snapshot", {
    headers: {
      Authorization: `Bearer ${session.access_token}`
    }
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const payload = await response.json();
  if ((payload.devices || []).length > 0) {
    renderSnapshot(payload);
  }
}

async function refreshDashboardHistory() {
  const session = getSession();
  if (!session) {
    byId("sessionStatus").textContent = "Session: signed out, login to load persisted history";
    return;
  }

  const response = await fetch("http://127.0.0.1:8080/api/dashboard/history?limit=10", {
    headers: {
      Authorization: `Bearer ${session.access_token}`
    }
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  renderHistory(await response.json());
}

function renderHistory(history) {
  const rows = [
    ...(history.telemetry || []).map((item) => ({
      label: item.device_id,
      kind: "telemetry",
      detail: `${item.health_state} cpu=${Number(item.cpu_percent).toFixed(1)}%`
    })),
    ...(history.diagnostics || []).map((item) => ({
      label: item.device_id,
      kind: "diagnostics",
      detail: `${item.severity} ${item.reason_code}`
    })),
    ...(history.recovery || []).map((item) => ({
      label: item.device_id,
      kind: "recovery",
      detail: `${item.action} ${item.result} attempt=${item.attempt}`
    })),
    ...(history.anomalies || []).map((item) => ({
      label: item.device_id,
      kind: "anomaly",
      detail: `${item.severity} score=${Number(item.score).toFixed(2)}`
    }))
  ];

  byId("historyCount").textContent = `${rows.length} records`;
  byId("historyList").innerHTML = rows.length
    ? rows.slice(0, 12).map(renderHistoryItem).join("")
    : `<div class="event"><strong>No persisted history</strong><p>Seed demo data to populate SQLite history.</p></div>`;
}

function renderHistoryItem(item) {
  return `
    <div class="event">
      <strong>${escapeHtml(item.label)} - ${escapeHtml(item.kind)}</strong>
      <p>${escapeHtml(item.detail)}</p>
    </div>
  `;
}

async function login(event) {
  event.preventDefault();
  const username = byId("usernameInput").value;
  const password = byId("passwordInput").value;
  const response = await fetch("http://127.0.0.1:8080/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) {
    byId("sessionStatus").textContent = "Session: login failed";
    return;
  }

  const payload = await response.json();
  sessionStorage.setItem(sessionKey, JSON.stringify(payload));
  updateSessionStatus();
  await refreshBackendHealth();
}

function logout() {
  sessionStorage.removeItem(sessionKey);
  updateSessionStatus();
  setDashboardVisible(false);
}

function getSession() {
  const raw = sessionStorage.getItem(sessionKey);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    sessionStorage.removeItem(sessionKey);
    return null;
  }
}

function updateSessionStatus() {
  const session = getSession();
  if (!session) {
    byId("sessionStatus").textContent = "Session: signed out";
    setDashboardVisible(false);
    return;
  }
  byId("sessionStatus").textContent = `Session: ${session.username} (${session.role})`;
  setDashboardVisible(true);
}

function setDashboardVisible(visible) {
  byId("loginView").classList.toggle("hidden", visible);
  byId("dashboardView").classList.toggle("hidden", !visible);
  byId("dashboardActions").classList.toggle("hidden", !visible);

  if (!visible && autoRefreshTimer) {
    clearInterval(autoRefreshTimer);
    autoRefreshTimer = null;
    byId("autoRefreshToggle").checked = false;
    byId("autoRefreshStatus").textContent = "Auto refresh: off";
  }
}

function toggleAutoRefresh() {
  const enabled = byId("autoRefreshToggle").checked;
  if (autoRefreshTimer) {
    clearInterval(autoRefreshTimer);
    autoRefreshTimer = null;
  }

  if (enabled) {
    autoRefreshTimer = setInterval(refreshBackendHealth, 5000);
    byId("autoRefreshStatus").textContent = "Auto refresh: every 5 seconds";
  } else {
    byId("autoRefreshStatus").textContent = "Auto refresh: off";
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
byId("historyButton").addEventListener("click", refreshDashboardHistory);
byId("mockButton").addEventListener("click", () => renderSnapshot(mockSnapshot));
byId("logoutButton").addEventListener("click", logout);
byId("loginForm").addEventListener("submit", login);
byId("autoRefreshToggle").addEventListener("change", toggleAutoRefresh);

updateSessionStatus();
refreshBackendHealth();
