from pydantic import BaseModel


class SystemStatusResponse(BaseModel):
    status: str
    environment: str
    database_backend: str
    database_path: str
    mqtt_host: str
    mqtt_port: int

