from trilium_py.client import ETAPI
from models import ExpandedNote, NoteAttribute, NoteExportData, NoteExport, Note
from datetime import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
import fnmatch
import os
import json


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


def get_notes_to_export(export: NoteExport, api: ETAPI) -> dict[str, NoteExportData]:
    seen = []
    queue = [export.id]
    results = {}
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
            not "image" in export.fileTypes or not "image" in export.noteTypes
        ):
            continue

        content_raw = api.get_note_content(proc)
        if type(content_raw) == str:
            content = content_raw
        else:
            content = urlsafe_b64encode(content_raw).decode()

        results[metadata.id] = NoteExportData(
                id=metadata.id,
                metadata=metadata,
                note_type=note_type,
                parents=metadata.parents,
                children=metadata.children,
                content=content,
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

def generate_note_subtree(notes: dict[str, NoteExportData], parent: str = None, parent_count: list[str] = []) -> list:
    valid_parents = []
    for note in notes.values():
        valid_parents.extend(note.parents)
    result = []
    ct = 1
    for note in notes.values():
        if parent in note.parents or (all([not i in valid_parents for i in note.parents]) and parent == None):
            result.append({
                "id": note.id,
                "title": note.metadata.title,
                "reference": [*parent_count, str(ct)],
                "children": generate_note_subtree(notes, parent=note.id, parent_count=[*parent_count, str(ct)])
            })
            ct += 1
    return result

def generate_html_toc(node: dict) -> str:
    return "<div class='toc-node'><a class='toc-node-title' href='#{node_id}'>{node_count} - {node_title}</a><div class='toc-node-children'>{node_children}</div></div>".format(
        node_id=node["id"],
        node_title=node["title"],
        node_children="".join([generate_html_toc(node["children"][i]) for i in range(len(node["children"]))]),
        node_count=".".join(node["reference"])
    )

def generate_html_content(notes: dict[str, NoteExportData], subtree: dict) -> str:
    note = notes[subtree["id"]]
    if note.metadata.type == "text":
        content = note.content
    elif note.metadata.type == "book":
        content = ""
    elif note.metadata.type == "code":
        content = f"<div class='content-code'>{note.content}</div>"
    elif note.metadata.type == "mermaid":
        content = f"<pre class='mermaid'>{note.content}</pre>"
    elif note.metadata.type == "canvas":
        content = json.loads(note.content)["svg"]
    elif note.metadata.type == "image":
        if note.metadata.mime_type == "image/svg+xml":
            content = "<svg" + note.content.split(">\n<svg")[1]
        else:
            content = f"<img src='data:{note.metadata.mime_type}{';base64' if not 'xml' in note.metadata.mime_type else ''},{note.content}'>"
    else:
        content = f"<div class='raw-content'>{note.content}</div>"
    
    return f"<div class='html-content'><h{len(subtree['reference']) if len(subtree['reference']) < 6 else 6}>{'.'.join(subtree['reference'])} - {note.metadata.title}</h{len(subtree['reference']) if len(subtree['reference']) < 6 else 6}><div class='contents'>{content}</div><div class='content-children'>{''.join([generate_html_content(notes, child) for child in subtree['children']])}</div></div>"

def generate_html_export(export: NoteExport, note_data: dict[str, NoteExportData], subtree: list[dict]) -> str:
    with open(os.path.join("template", "template.html"), "r") as template:
        tmpstr = template.read()

    return tmpstr.format(
        _title=export.title,
        _toc="".join([generate_html_toc(subtree[i]) for i in range(len(subtree))]),
        _content="".join([generate_html_content(note_data, i) for i in subtree])
    ).replace("$$$<", "{").replace(">$$$", "}")