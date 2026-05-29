from fastapi import APIRouter

from backend.models.dashboard import DashboardSnapshotResponse
from backend.services.event_store import event_store

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/snapshot", response_model=DashboardSnapshotResponse)
def get_dashboard_snapshot() -> DashboardSnapshotResponse:
    return event_store.snapshot()

