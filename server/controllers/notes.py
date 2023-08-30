from litestar import Controller, get, post
from litestar.exceptions import *
from models import AppState, Note, ExpandedNote, NoteAttribute, TriliumStatus
from datetime import datetime
from typing import Union
from litestar.response import Response
from util.notes import expand_note
from util.guards import guard_scope


class NotesController(Controller):
    path = "/notes"
    guards = [guard_scope(["privileged", "unprivileged"])]

    @get("/status")
    async def get_trilium_status(self, app_state: AppState) -> TriliumStatus:
        try:
            info = app_state.api.app_info()
            return TriliumStatus(
                online=True,
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
            return TriliumStatus(online=False)

    @get("/{note_id:str}")
    async def get_note(self, note_id: str, app_state: AppState) -> Note:
        try:
            note = app_state.api.get_note(note_id)
        except:
            raise NotFoundException(detail="Invalid note ID")
        return Note(
            id=note["noteId"],
            protected=note["isProtected"],
            title=note["title"],
            type=note["type"],
            mime_type=note["mime"],
            created=datetime.fromisoformat(note["dateCreated"]),
            modified=datetime.fromisoformat(note["dateModified"]),
            utc_created=datetime.fromisoformat(note["utcDateCreated"]),
            utc_modified=datetime.fromisoformat(note["utcDateModified"]),
            children=[i for i in note["childNoteIds"] if not "_" in i],
            parents=[i for i in note["parentNoteIds"] if not "_" in i],
            attributes=[
                NoteAttribute(
                    id=a["attributeId"],
                    note_id=a["noteId"],
                    type=a["type"],
                    name=a["name"],
                    value=a["value"],
                    utc_modified=datetime.fromisoformat(a["utcDateModified"]),
                )
                for a in note["attributes"]
            ],
        )
    
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
    
    @get("/{note_id:str}/expanded")
    async def get_note_expanded(self, note_id: str, app_state: AppState) -> ExpandedNote:
        try:
            return expand_note(note_id, app_state.api)
        except:
            raise NotFoundException(detail="Invalid note ID")
