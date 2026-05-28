from fastapi import FastAPI

from backend.api.diagnostics import router as diagnostics_router
from backend.api.recovery import router as recovery_router
from backend.api.telemetry import router as telemetry_router

app = FastAPI(
    title="Ring IoT Reliability Backend",
    description="Telemetry ingestion and reliability service API.",
    version="0.1.0",
)

app.include_router(telemetry_router, prefix="/api")
app.include_router(diagnostics_router, prefix="/api")
app.include_router(recovery_router, prefix="/api")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
