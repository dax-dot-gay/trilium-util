from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class NoteAttribute(BaseModel):
    id: str
    note_id: str
    type: str
    name: str
    value: str
    utc_modified: datetime

    @classmethod
    def from_api(cls, a: dict) -> "NoteAttribute":
        return NoteAttribute(id=a["attributeId"],
                    note_id=a["noteId"],
                    type=a["type"],
                    name=a["name"],
                    value=a["value"],
                    utc_modified=datetime.fromisoformat(a["utcDateModified"]))

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

    @classmethod
    def from_api(cls, note: dict) -> "Note":
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
                NoteAttribute.from_api(a)
                for a in note["attributes"]
            ],
        )

class ExpandedNote(BaseModel):
    id: str
    protected: bool
    title: str
    type: str
    mime_type: str
    attributes: list[NoteAttribute]
    children: list["ExpandedNote"]

class NoteExport(BaseModel):
    id: str
    title: str
    exportChildren: bool
    exportRelations: bool
    noteTypes: list[str]
    fileTypes: list[str]
    mimeTypeMapping: dict[str, dict[str, list[str]]]

class NoteExportData(BaseModel):
    id: str
    metadata: Note
    note_type: Literal["text", "book", "code", "mermaid", "canvas", "file.plaintext", "file.image", "file.html"]
    parents: list[str]
    children: list[str]
    content: str
