from pydantic import BaseModel
from typing import Any
from datetime import datetime

class NoteAttribute(BaseModel):
    id: str
    note_id: str
    type: str
    name: str
    value: str
    utc_modified: datetime

class Note(BaseModel):
    id: str
    protected: bool
    title: str
    type: str
    mime_type: str
    created: datetime
    modified: datetime
    utc_created: datetime
    utc_modified: datetime
    children: list[str]
    parents: list[str]
    attributes: list[NoteAttribute]

class ExpandedNote(BaseModel):
    id: str
    protected: bool
    title: str
    type: str
    mime_type: str
    attributes: list[NoteAttribute]
    children: list["ExpandedNote"]
