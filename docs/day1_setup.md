# Day 1 Setup

## Day 1 Accomplishments

- Created the initial repository foundation for an embedded Linux and IoT reliability platform.
- Established top-level project domains for device simulation, backend services, dashboard UI, AI engine, Docker, scripts, tests, tools, and documentation.
- Added a C++17 simulator skeleton with reliability-focused class boundaries.
- Added a FastAPI backend starter with telemetry ingestion structure.
- Added AI anomaly detection placeholder modules.
- Added Qt dashboard architecture placeholder.
- Added Docker placeholders for backend, MQTT broker, and dashboard.
- Added PowerShell scripts for setup, C++ build, and backend startup.
- Added initial roadmap, architecture notes, and interview talking points.

## Setup Checklist

```powershell
# From repository root
.\scripts\setup_env.ps1

# Build C++ simulator skeleton
.\scripts\build_cpp.ps1

# Run simulator telemetry snapshots from config
.\device_simulator\build\Debug\device_simulator.exe .\device_simulator\config\device_config.example.json

# Start backend API
.\scripts\run_backend.ps1

# Start MQTT broker later, after docker compose is expanded
docker compose -f .\docker\docker-compose.yml up mqtt-broker
```

## Next Steps

- Start Week 3 MQTT client abstraction.
- Map simulator telemetry JSON to MQTT publish topics.
- Add backend MQTT subscriber design before implementation.
- Add backend data contracts for telemetry and diagnostics events.
- Decide whether local persistence begins with SQLite, PostgreSQL, or time-series storage.

## Known Risks And Open Questions

- MQTT authentication and device identity strategy are not defined yet.
- Telemetry schema versioning should be designed before real payloads are introduced.
- Recovery actions must avoid repeated restart loops.
- AI anomaly detection needs realistic sample data before model design is meaningful.
- Dashboard transport should be decided: REST polling first or WebSocket streaming.
- Test framework choices for C++ are still open.
