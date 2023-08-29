from trilium_py.client import ETAPI
from models import ExpandedNote, NoteAttribute
from datetime import datetime

def expand_note(root: str, api: ETAPI) -> ExpandedNote:
    note = api.get_note(root)
    return ExpandedNote(
        id=note["noteId"],
        protected=note["isProtected"],
        title=note["title"],
        type=note["type"],
        mime_type=note["mime"],
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
        children=[expand_note(i, api) for i in note["childNoteIds"] if not "_" in i]
    )