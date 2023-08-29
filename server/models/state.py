from pydantic import BaseModel, ConfigDict
from typing_extensions import TypedDict
from trilium_py.client import ETAPI
from litestar.stores.base import Store
from litestar.datastructures import State

class AppEnvironment(TypedDict):
    TRU_SERVER: str
    TRU_ETAPI_TOKEN: str
    TRU_PASSWORD: str
    TRU_PASSWORDLESS_VIEWING: str

class AppState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    env: AppEnvironment
    api: ETAPI
    view_passwordless: bool
    session_store: Store

    @classmethod
    def from_state(cls, state: State) -> "AppState":
        return AppState(env=state.env, api=state.api, view_passwordless=state.view_passwordless, session_store=state.session_store)