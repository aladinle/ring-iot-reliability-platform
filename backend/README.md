# Backend Service

FastAPI backend for telemetry ingestion, diagnostics coordination, alert processing, and dashboard-facing APIs.

## Planned Service Boundaries

- api: HTTP route definitions.
- models: Pydantic request and response contracts.
- services: Application logic and orchestration.
- telemetry: Telemetry normalization and ingestion workflows.
- alerts: Alert classification and routing.
- database: Persistence adapters.

## Run

```powershell
.\scripts\run_backend.ps1
```

