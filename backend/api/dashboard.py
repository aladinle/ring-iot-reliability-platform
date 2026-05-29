from fastapi import APIRouter, Depends

from backend.api.auth import require_session
from backend.models.dashboard import DashboardSnapshotResponse
from backend.services.event_store import event_store

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/snapshot", response_model=DashboardSnapshotResponse, dependencies=[Depends(require_session)])
def get_dashboard_snapshot() -> DashboardSnapshotResponse:
    return event_store.snapshot()
