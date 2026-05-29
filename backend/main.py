from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.anomaly import router as anomaly_router
from backend.api.auth import router as auth_router
from backend.api.dashboard import router as dashboard_router
from backend.api.diagnostics import router as diagnostics_router
from backend.api.recovery import router as recovery_router
from backend.api.system import router as system_router
from backend.api.telemetry import router as telemetry_router

app = FastAPI(
    title="Ring IoT Reliability Backend",
    description="Telemetry ingestion and reliability service API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telemetry_router, prefix="/api")
app.include_router(diagnostics_router, prefix="/api")
app.include_router(recovery_router, prefix="/api")
app.include_router(anomaly_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(system_router, prefix="/api")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
