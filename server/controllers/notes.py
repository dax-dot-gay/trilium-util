from litestar import Controller, get, post
from litestar.exceptions import *
from models import AppState, Note, ContentNote, ExpandedNote, NoteAttribute
from datetime import datetime


class NotesController(Controller):
    path = "/notes"

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
    async def get_note(self, note_id: str, app_state: AppState) -> Note:
        try:
            note = app_state.api.get_note(note_id)
        except:
            raise NotFoundException(detail="Invalid note ID")
        try:
            content = app_state.api.get_note_content(note_id)
        except Exception as e:
            print(e.with_traceback)
            raise MethodNotAllowedException(detail="Invalid data type")
        return ContentNote(
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
            content=content
        )
