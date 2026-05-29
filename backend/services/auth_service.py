from secrets import token_urlsafe

from fastapi import HTTPException, status

from backend.models.auth import LoginRequest, LoginResponse, SessionUser


class AuthService:
    def __init__(self) -> None:
        self._users = {
            "operator": {"password": "operator123", "role": "operator"},
            "admin": {"password": "admin123", "role": "admin"},
        }
        self._sessions: dict[str, SessionUser] = {}

    def login(self, payload: LoginRequest) -> LoginResponse:
        user = self._users.get(payload.username)
        if user is None or user["password"] != payload.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        token = token_urlsafe(24)
        session = SessionUser(username=payload.username, role=user["role"])
        self._sessions[token] = session
        return LoginResponse(
            access_token=token,
            username=session.username,
            role=session.role,
        )

    def get_session(self, token: str) -> SessionUser:
        session = self._sessions.get(token)
        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
            )
        return session

    def clear(self) -> None:
        self._sessions.clear()


auth_service = AuthService()

