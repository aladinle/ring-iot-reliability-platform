import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from backend.database.repository import EventRepository
from backend.models.dashboard import AlertState, AnomalyState, DeviceStatus, RecoveryState


class SQLiteEventRepository(EventRepository):
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self._lock = Lock()

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS telemetry_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    health_state TEXT NOT NULL,
                    cpu_percent REAL NOT NULL,
                    memory_percent REAL NOT NULL,
                    temperature_celsius REAL NOT NULL,
                    uptime_seconds INTEGER NOT NULL,
                    observed_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS diagnostics_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    health_state TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    reason_code TEXT NOT NULL,
                    recommended_action TEXT NOT NULL,
                    observed_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS recovery_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    result TEXT NOT NULL,
                    attempt INTEGER NOT NULL,
                    reason_code TEXT NOT NULL,
                    observed_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS anomaly_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    score REAL NOT NULL,
                    reason TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    is_anomaly INTEGER NOT NULL,
                    observed_at TEXT NOT NULL
                );
                """
            )

    def clear(self) -> None:
        with self._lock, self._connect() as connection:
            for table in (
                "telemetry_events",
                "diagnostics_events",
                "recovery_events",
                "anomaly_events",
            ):
                connection.execute(f"DELETE FROM {table}")

    def record_telemetry(self, device: DeviceStatus) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO telemetry_events (
                    device_id, health_state, cpu_percent, memory_percent,
                    temperature_celsius, uptime_seconds, observed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    device.device_id,
                    device.health_state,
                    device.cpu_percent,
                    device.memory_percent,
                    device.temperature_celsius,
                    device.uptime_seconds,
                    self._now(),
                ),
            )

    def record_diagnostics(self, alert: AlertState, health_state: str) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO diagnostics_events (
                    device_id, health_state, severity, reason_code,
                    recommended_action, observed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    alert.device_id,
                    health_state,
                    alert.severity,
                    alert.reason_code,
                    alert.recommended_action,
                    self._now(),
                ),
            )

    def record_recovery(self, recovery: RecoveryState, reason_code: str) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO recovery_events (
                    device_id, action, result, attempt, reason_code, observed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    recovery.device_id,
                    recovery.action,
                    recovery.result,
                    recovery.attempt,
                    reason_code,
                    self._now(),
                ),
            )

    def record_anomaly(self, anomaly: AnomalyState) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO anomaly_events (
                    device_id, score, reason, severity, is_anomaly, observed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    anomaly.device_id,
                    anomaly.score,
                    anomaly.reason,
                    anomaly.severity,
                    1 if anomaly.is_anomaly else 0,
                    self._now(),
                ),
            )

    def history(self, limit: int = 100) -> dict[str, list[dict[str, object]]]:
        limit = max(1, min(limit, 500))
        with self._lock, self._connect() as connection:
            return {
                "telemetry": self._query(connection, "telemetry_events", limit),
                "diagnostics": self._query(connection, "diagnostics_events", limit),
                "recovery": self._query(connection, "recovery_events", limit),
                "anomalies": self._query(connection, "anomaly_events", limit),
            }

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _query(self, connection: sqlite3.Connection, table: str, limit: int) -> list[dict[str, object]]:
        cursor = connection.execute(
            f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        for row in rows:
            if "is_anomaly" in row:
                row["is_anomaly"] = bool(row["is_anomaly"])
        return rows

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

