import { useEffect, useMemo, useState } from "react";
import { Note } from "../../types/note";
import { useApiFunctions } from "../../hooks/api";
import { Paper } from "@mantine/core";
import * as BoxIcons from "react-icons/bi";
import { MdQuestionMark } from "react-icons/md";

export function NoteIcon({ note, size }: { note: Note; size?: number }) {
    const IconComponent = useMemo(() => {
        const iconClassAttr = note.attributes.find(
            (attr) => attr.name === "iconClass"
        );
        if (iconClassAttr) {
            const [version, ...className] = iconClassAttr.value
                .split(" ")[1]
                .split("-");
            const capitalizedClass = className
                .map((word) => word[0].toUpperCase() + word.slice(1))
                .join("");
            return (BoxIcons as any)[
                version === "bx"
                    ? `Bi${capitalizedClass}`
                    : `BiSolid${capitalizedClass}`
            ];
        } else {
            return MdQuestionMark;
        }
    }, [note]);
    return <IconComponent size={size} className="note-icon" />;
}

export function NoteNode({ id }: { id: string }) {
    const [metadata, setMetadata] = useState<Note | null>(null);
    const [expanded, setExpanded] = useState(false);
    const [showChildren, setShowChildren] = useState(false);
    const { get } = useApiFunctions();

    useEffect(() => {
        get<Note>(`/notes/${id}`).then((result) =>
            result.success ? setMetadata(result.value) : setMetadata(null)
        );
    }, [id]);

    useEffect(() => {
        if (!showChildren && expanded) {
            setShowChildren(true);
        }
    }, [expanded]);

    return metadata ? (
        <Paper p="sm" radius="sm" className="note-node"></Paper>
    ) : (
        <></>
    );
}
