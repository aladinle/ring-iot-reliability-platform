from fastapi import FastAPI

from backend.api.telemetry import router as telemetry_router

app = FastAPI(
    title="Ring IoT Reliability Backend",
    description="Telemetry ingestion and reliability service API.",
    version="0.1.0",
)

app.include_router(telemetry_router, prefix="/api")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
