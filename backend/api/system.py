from fastapi import APIRouter

from backend.core.config import settings
from backend.models.system import SystemStatusResponse

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status", response_model=SystemStatusResponse)
def system_status() -> SystemStatusResponse:
    return SystemStatusResponse(
        status="healthy",
        environment=settings.environment,
        database_backend=settings.database_backend,
        database_path=settings.database_path,
        mqtt_host=settings.mqtt_host,
        mqtt_port=settings.mqtt_port,
    )

