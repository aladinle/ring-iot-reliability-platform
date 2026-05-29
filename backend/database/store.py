from pathlib import Path

from backend.core.config import settings
from backend.database.sqlite_repository import SQLiteEventRepository


def default_database_path() -> Path:
    return Path(settings.database_path)


event_repository = SQLiteEventRepository(default_database_path())
event_repository.initialize()
