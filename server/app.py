from models import AppState, AppEnvironment
from controllers import *
from dotenv import load_dotenv
from os import getenv
from trilium_py.client import ETAPI
from litestar import Litestar
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

api = ETAPI(environment["TRU_SERVER"], environment["TRU_ETAPI_TOKEN"])
sessions = MemoryStore()


async def depends_state(state: State) -> AppState:
    return AppState.from_state(state)


app = Litestar(
    route_handlers=[NotesController],
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
