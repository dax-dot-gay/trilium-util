from util.etapi import ExtendedETAPI
from util.notes import *
from models import NoteExport
from dotenv import load_dotenv
from os import getenv, makedirs, path
import json

load_dotenv()

EXPORT = NoteExport(
    id="root",
    title="Test Export",
    exportChildren=True,
    exportRelations=True,
    noteTypes=["text", "book", "code", "mermaid", "canvas", "image", "file"],
    fileTypes=["plaintext", "image", "html"],
    mimeTypeMapping={
    "plaintext": {
        "mimeTypes": ["text/*", "application/json", "application/xml"],
        "excludeMimeTypes": ["text/html"]
    },
    "image": {
        "mimeTypes": ["image/*"],
        "excludeMimeTypes": []
    },
    "html": {
        "mimeTypes": ["text/html"],
        "excludeMimeTypes": []
    }
}
)

api = ExtendedETAPI(getenv("TRU_SERVER"), getenv("TRU_ETAPI_TOKEN"))
makedirs("./test", exist_ok=True)

export_data = get_notes_to_export(EXPORT, api)
with open(path.join("test", "exportData.json"), "w") as f:
    json.dump({k: json.loads(i.model_dump_json()) for k, i in export_data.items()}, f, indent=4)

export_subtree = generate_note_subtree(export_data)
with open(path.join("test", "exportSubtree.json"), "w") as f:
    json.dump(export_subtree, f, indent=4)

export_html = generate_html_export(EXPORT, export_data, export_subtree)
with open(path.join("test", "exportHTML.html"), "w") as f:
    f.write(export_html)
