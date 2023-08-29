from models import AppState, AppEnvironment
from controllers import *
from dotenv import load_dotenv
from os import getenv
from util.etapi import ExtendedETAPI
from litestar import Litestar, MediaType, Request, Response
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.stores.memory import MemoryStore
from litestar.datastructures import State
from litestar.di import Provide

load_dotenv()

environment: AppEnvironment = {
    "TRU_SERVER": getenv("TRU_SERVER"),
    "TRU_ETAPI_TOKEN": getenv("TRU_ETAPI_TOKEN"),
    "TRU_PASSWORD": getenv("TRU_PASSWORD", "password"),
    "TRU_PASSWORDLESS_VIEWING": getenv("TRU_PASSWORDLESS_VIEWING", "false"),
}

api = ExtendedETAPI(environment["TRU_SERVER"], environment["TRU_ETAPI_TOKEN"])
sessions = MemoryStore()


async def depends_state(state: State) -> AppState:
    return AppState.from_state(state)

def error_handler(req: Request, exc: Exception) -> Response:
    """Default handler for exceptions subclassed from HTTPException."""
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", "")

    req.app.logger.exception("Encountered server error:\n")

    return Response(
        media_type=MediaType.TEXT,
        content=detail,
        status_code=status_code,
    )


app = Litestar(
    route_handlers=[NotesController, AuthController],
    exception_handlers={500: error_handler},
    state=State(
        {
            "env": environment,
            "api": api,
            "view_passwordless": True
            if environment["TRU_PASSWORDLESS_VIEWING"] == "true"
            else False,
            "session_store": sessions,
        }
    ),
    dependencies={"app_state": Provide(depends_state)},
)
