from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler
from typing import Literal
from models import AppState

SECURITY_SCOPE = Literal["privileged", "unprivileged", "anonymous"]

def guard_scope(scopes: list[SECURITY_SCOPE]):
    async def guard_scope_internal(connection: ASGIConnection, _: BaseRouteHandler) -> None:
        state = AppState.from_state(connection.app.state)
        session_token = connection.headers.get("authorization")
        scope: SECURITY_SCOPE
        if not session_token:
            scope = "unprivileged" if state.view_passwordless else "anonymous"
        elif await state.session_store.get(session_token) != "true".encode():
            scope = "unprivileged" if state.view_passwordless else "anonymous"
        else:
            scope = "privileged"
        if not scope in scopes:
            raise NotAuthorizedException(detail="You are not authorized to access this endpoint.")
    return guard_scope_internal
        

