from litestar import Controller, get, post
from litestar.exceptions import *
from models import AppState, Note, ExpandedNote, NoteAttribute, TriliumStatus, NoteExport
from datetime import datetime
import os
from litestar.response import Response, File
from util.notes import *
from util.guards import guard_scope
from secrets import token_urlsafe


class NotesController(Controller):
    path = "/notes"

    @get("/status", guards=[guard_scope(["privileged", "unprivileged"])])
    async def get_trilium_status(self, app_state: AppState) -> TriliumStatus:
        try:
            info = app_state.api.app_info()
            return TriliumStatus(
                online=True,
                url=app_state.api.server_url,
                appVersion=info["appVersion"],
                dbVersion=info["dbVersion"],
                syncVersion=info["syncVersion"],
                buildDate=datetime.fromisoformat(info["buildDate"]),
                buildRevision=info["buildRevision"],
                dataDirectory=info["dataDirectory"],
                clipperProtocolVersion=info["clipperProtocolVersion"],
                utcDateTime=datetime.fromisoformat(info["utcDateTime"])
            )
        except:
            return TriliumStatus(online=False, url=app_state.api.server_url,)

    @get("/{note_id:str}", guards=[guard_scope(["privileged", "unprivileged"])])
    async def get_note(self, note_id: str, app_state: AppState) -> Note:
        try:
            note = app_state.api.get_note(note_id)
        except:
            raise NotFoundException(detail="Invalid note ID")
        return Note.from_api(note)
    
    @get("/{note_id:str}/content")
    async def get_note_content(self, note_id: str, app_state: AppState) -> Response:
        try:
            note = app_state.api.get_note(note_id)
        except:
            raise NotFoundException(detail="Invalid note ID")
        try:
            content = app_state.api.get_note_content(note_id)
        except Exception as e:
            print(e)
            raise MethodNotAllowedException(detail="Invalid data type")
        
        return Response(content, media_type=note["mime"], status_code=200)
    
    @get("/{note_id:str}/expanded", guards=[guard_scope(["privileged", "unprivileged"])])
    async def get_note_expanded(self, note_id: str, app_state: AppState) -> ExpandedNote:
        try:
            return expand_note(note_id, app_state.api)
        except:
            raise NotFoundException(detail="Invalid note ID")
    
    @post("/{note_id:str}/export", guards=[guard_scope(["privileged"])])
    async def export_note(self, app_state: AppState, data: NoteExport) -> dict:
        export_data =  get_notes_to_export(data, app_state.api)
        export_subtree = generate_note_subtree(export_data)
        raw_html = generate_html_export(data, export_data, export_subtree)
        translated_html = translate_html_export_links(raw_html, export_data)
        os.makedirs("exports", exist_ok=True)
        export_id = token_urlsafe(8)
        with open(os.path.join("exports", f"export_{export_id}.html"), "w") as f:
            f.write(translated_html)
        return {"id": export_id}
    
    @get("/exports/{export:str}")
    async def get_exported_note(self, export: str) -> File:
        if not os.path.exists(os.path.join("exports", f"export_{export}.html")):
            raise NotFoundException(detail="Export does not exist")
        return File(os.path.join("exports", f"export_{export}.html"), media_type="text/html", filename=f"export_{export}.html")
        

