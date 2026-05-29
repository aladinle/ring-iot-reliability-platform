import os
from pathlib import Path

from backend.database.sqlite_repository import SQLiteEventRepository


def default_database_path() -> Path:
    configured = os.getenv("RING_IOT_DB_PATH")
    if configured:
        return Path(configured)
    return Path("data") / "ring_iot.db"


event_repository = SQLiteEventRepository(default_database_path())
event_repository.initialize()

