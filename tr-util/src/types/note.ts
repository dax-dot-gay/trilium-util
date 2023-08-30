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
    type: string;
    mime_type: string;
    created: string;
    modified: string;
    utc_created: string;
    utc_modified: string;
    children: string[];
    parents: string[];
    attributes: NoteAttribute[];
};