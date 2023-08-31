export type NoteTypeExportable = "text" | "book" | "code" | "mermaid" | "canvas" | "image" | "file";
export type NoteType = NoteTypeExportable | "webView";
export const noteTypesExportable = ["text", "book", "code", "mermaid", "canvas", "image", "file"];
export type FileTypes = "plaintext" | "image" | "html";
export const fileTypesFeatures: {
    [key in FileTypes]: {
        mimeTypes: `${string}/${string}`[];
        excludeMimeTypes: `${string}/${string}`[];
    }
} = {
    plaintext: {
        mimeTypes: ["text/*", "application/json", "application/xml"],
        excludeMimeTypes: ["text/html"]
    },
    image: {
        mimeTypes: ["image/*"],
        excludeMimeTypes: []
    },
    html: {
        mimeTypes: ["text/html"],
        excludeMimeTypes: []
    }
}

export type NoteAttribute = {
    id: string;
    note_id: string;
    type: string;
    name: string;
    value: string;
    utc_modified: string;
};

export type Note = {
    id: string;
    protected: string;
    title: string;
    type: NoteType;
    mime_type: string;
    created: string;
    modified: string;
    utc_created: string;
    utc_modified: string;
    children: string[];
    parents: string[];
    attributes: NoteAttribute[];
};