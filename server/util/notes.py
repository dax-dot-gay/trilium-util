from trilium_py.client import ETAPI
from models import ExpandedNote, NoteAttribute, NoteExportData, NoteExport, Note
from datetime import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
import fnmatch


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
        children=[expand_note(i, api) for i in note["childNoteIds"] if not "_" in i],
    )


def get_notes_to_export(export: NoteExport, api: ETAPI) -> list[NoteExportData]:
    seen = []
    queue = [export.id]
    results = []
    while len(queue) > 0:
        proc = queue.pop(0)
        seen.append(proc)
        metadata = Note.from_api(api.get_note(proc))
        note_type = None
        if metadata.type in ["text", "book", "code", "mermaid", "canvas"]:
            note_type = metadata.type
        elif metadata.type == "image":
            note_type = "file.image"
        elif metadata.type == "file":
            for file_type, mime_types in export.mimeTypeMapping.items():
                if not metadata.mime_type in mime_types["excludeMimeTypes"] and any(
                    [
                        fnmatch.fnmatch(metadata.mime_type, mime)
                        for mime in mime_types["mimeTypes"]
                    ]
                ):
                    note_type = f"file.{file_type}"
                    break
            if not note_type:
                continue
        else:
            continue
        
        if not metadata.type in ["text", "book", "code", "mermaid", "canvas", "file", "image"]:
            continue

        if (
            metadata.type in ["text", "book", "code", "mermaid", "canvas"]
            and not metadata.type in export.noteTypes
        ):
            continue
        if metadata.type == "file" and (
            not note_type.split(".")[1] in export.fileTypes
            or not "file" in export.noteTypes
        ):
            continue
        if metadata.type == "image" and (
            not "file.image" in export.fileTypes or not "image" in export.noteTypes
        ):
            continue

        content_raw = api.get_note_content(proc)
        if type(content_raw) == str:
            content = content_raw
        else:
            content = urlsafe_b64encode(content_raw).decode()

        results.append(
            NoteExportData(
                id=metadata.id,
                metadata=metadata,
                note_type=note_type,
                parents=metadata.parents,
                children=metadata.children,
                content=content,
            )
        )

        if export.exportChildren:
            queue.extend([c for c in metadata.children if not c in seen])
        if export.exportRelations:
            queue.extend(
                [
                    c
                    for c in [
                        attr.value
                        for attr in metadata.attributes
                        if attr.type == "relation"
                    ]
                    if not c in seen
                ]
            )

    return results
