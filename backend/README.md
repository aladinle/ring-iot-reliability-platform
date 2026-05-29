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

## Endpoints

```text
GET  /health
POST /api/auth/login
GET  /api/auth/me
POST /api/telemetry/ingest
POST /api/diagnostics/ingest
POST /api/recovery/ingest
POST /api/anomaly/score
GET  /api/dashboard/snapshot
```

The dashboard snapshot endpoint is backed by an in-memory event store for local demos. It is intentionally simple and can be replaced by durable storage later.

Demo credentials:

```text
operator / operator123
admin    / admin123
```
