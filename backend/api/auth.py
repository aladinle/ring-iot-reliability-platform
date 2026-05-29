from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.models.auth import LoginRequest, LoginResponse, SessionUser
from backend.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer()


def require_session(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> SessionUser:
    return auth_service.get_session(credentials.credentials)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    return auth_service.login(payload)


@router.get("/me", response_model=SessionUser)
def me(session: SessionUser = Depends(require_session)) -> SessionUser:
    return session

