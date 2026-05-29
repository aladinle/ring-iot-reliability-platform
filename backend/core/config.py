from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    app_name: str = "Ring IoT Reliability Backend"
    environment: str = getenv("RING_IOT_ENV", "local")
    mqtt_host: str = getenv("MQTT_HOST", "localhost")
    mqtt_port: int = int(getenv("MQTT_PORT", "1883"))
    database_backend: str = getenv("DATABASE_BACKEND", "sqlite")
    database_path: str = getenv("RING_IOT_DB_PATH", "data/ring_iot.db")


settings = Settings()

