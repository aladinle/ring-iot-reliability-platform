# Database Persistence

The backend now stores reliability events in SQLite while keeping service code behind a repository boundary.

## Current Storage

Default database path:

```text
data/ring_iot.db
```

Stored tables:

```text
telemetry_events
diagnostics_events
recovery_events
anomaly_events
```

History endpoint:

```text
GET /api/dashboard/history
```

This endpoint requires a dashboard session token.

## Why SQLite First

SQLite keeps local development simple:

- no database server required
- deterministic tests
- easy demo setup
- good schema proving ground

## MySQL Migration Path

The backend writes through `backend/database/repository.py`, so a future MySQL implementation can be added without changing service-layer behavior.

Planned structure:

```text
backend/database/repository.py
backend/database/sqlite_repository.py
backend/database/mysql_repository.py
backend/database/store.py
```

Future config:

```env
DATABASE_BACKEND=sqlite
DATABASE_URL=sqlite:///data/ring_iot.db
```

Later:

```env
DATABASE_BACKEND=mysql
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/ring_iot
```

## Manual Test

Start backend:

```powershell
.\scripts\run_backend.ps1 -Port 8080
```

Seed demo data:

```powershell
.\scripts\seed_demo_data.ps1 -Port 8080
```

Login:

```powershell
$login = Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/auth/login" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"username":"operator","password":"operator123"}'
```

Fetch history:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/dashboard/history" `
  -Headers @{ Authorization = "Bearer $($login.access_token)" }
```

