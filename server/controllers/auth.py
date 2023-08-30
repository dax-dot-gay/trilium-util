from litestar import Controller, get, post, Request
from litestar.di import Provide
from models import AppState
from pydantic import BaseModel
from secrets import token_urlsafe
from typing import Union
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler

class AuthRequiredModel(BaseModel):
    required: bool

class SessionModel(BaseModel):
    token: str
    logged_in: bool

SESSION_TYPE = Union[SessionModel, None]

async def dep_session(request: Request, app_state: AppState) -> SESSION_TYPE:
    current_token = request.headers.get("authorization", None)
    if current_token:
        logged_in = await app_state.session_store.get(current_token, renew_for=86400)
        if logged_in != None:
            return SessionModel(token=current_token, logged_in=logged_in.decode() == "true")
    return None

async def guard_session(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    current_token = connection.headers.get("authorization", None)
    if not current_token:
        raise NotAuthorizedException(detail="This endpoint requires valid authorization: Session")
    logged_in = await connection.app.state.session_store.get(current_token, renew_for=86400)
    if logged_in == "false":
        raise NotAuthorizedException(detail="This endpoint requires valid authorization: Session")

class AuthController(Controller):
    path = "/auth"
    dependencies = {"session": Provide(dep_session)}

    @get("/required")
    async def check_if_auth_required_for_viewing(self, app_state: AppState) -> AuthRequiredModel:
        return AuthRequiredModel(required=app_state.view_passwordless)
    
    @get("/")
    async def get_session(self, app_state: AppState, session: SESSION_TYPE) -> SessionModel:
        if session:
            return session
        
        new_token = token_urlsafe(32)
        await app_state.session_store.set(new_token, "false", expires_in=86400)
        return SessionModel(
            token=new_token,
            logged_in=False
        )
    
    @post("/login", guards=[guard_session])
    async def login(self, app_state: AppState, data: dict[str, str], session: SESSION_TYPE) -> SessionModel:
        if app_state.env["TRU_PASSWORD"] != data["password"]:
            raise NotAuthorizedException(detail="Incorrect password")
        app_state.session_store.set(session.token, "true", expires_in=86400)
        return SessionModel(
            token=session.token,
            logged_in=True
        )
    
    @post("/logout", guards=[guard_session])
    async def login(self, app_state: AppState, session: SESSION_TYPE) -> SessionModel:
        app_state.session_store.set(session.token, "false", expires_in=86400)
        return SessionModel(
            token=session.token,
            logged_in=False
        )