# Database Layer

Persistence uses a repository boundary so SQLite can be used locally and MySQL can be added later without rewriting backend services.

Current implementation:

- `repository.py`: storage interface.
- `sqlite_repository.py`: SQLite implementation.
- `store.py`: configured repository singleton.

Default database path:

```text
data/ring_iot.db
```

Override for local runs or tests:

```powershell
$env:RING_IOT_DB_PATH="data/custom.db"
```

