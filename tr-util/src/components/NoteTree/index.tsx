import { useEffect, useMemo, useState } from "react";
import { Note } from "../../types/note";
import { useApiFeatures, useApiFunctions } from "../../hooks/api";
import {
    ActionIcon,
    Collapse,
    Group,
    Paper,
    Skeleton,
    Stack,
    Text,
    useMantineTheme,
} from "@mantine/core";
import * as BoxIcons from "react-icons/bi";
import { MdCloudDownload, MdExpandLess, MdExpandMore } from "react-icons/md";
import { ExportModal } from "../ExportModal";

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
            if (note.title === "root") {
                return BoxIcons["BiChevronsRight"];
            } else {
                switch (note.type) {
                    case "text":
                        return note.children.length === 0
                            ? BoxIcons["BiNote"]
                            : BoxIcons["BiFolder"];
                    case "book":
                        return BoxIcons["BiBook"];
                    case "code":
                        return BoxIcons["BiCode"];
                    case "mermaid":
                        return BoxIcons["BiSelection"];
                    case "canvas":
                        return BoxIcons["BiPen"];
                    case "webView":
                        return BoxIcons["BiGlobeAlt"];
                    case "image":
                        return BoxIcons["BiImage"];
                    case "file":
                        return BoxIcons["BiFile"];
                    default:
                        return BoxIcons["BiQuestionMark"];
                }
            }
        }
    }, [note]);
    return <IconComponent size={size} className="note-icon" />;
}

export function NoteNode({ id }: { id: string }) {
    const [metadata, setMetadata] = useState<Note | null>(null);
    const [expanded, setExpanded] = useState(false);
    const { get } = useApiFunctions();
    const theme = useMantineTheme();
    const { loggedIn } = useApiFeatures();
    const [exporting, setExporting] = useState<Note | null>(null);

    useEffect(() => {
        get<Note>(`/notes/${id}`).then((result) =>
            result.success ? setMetadata(result.value) : setMetadata(null)
        );
    }, [id]);

    return metadata ? (
        <Paper
            p="xs"
            radius="sm"
            className="note-node"
            style={{
                borderLeft: "1px solid " + theme.colors.gray[7],
            }}
            shadow="sm"
        >
            <Stack spacing="md">
                <Group position="apart" className="note-header">
                    <Group spacing="sm">
                        <NoteIcon note={metadata} size={24} />
                        <Text className="note-title" size={16}>
                            {metadata.title}
                        </Text>
                    </Group>
                    <Group spacing="md">
                        {loggedIn && (
                            <ActionIcon
                                size="lg"
                                onClick={() => setExporting(metadata)}
                            >
                                <MdCloudDownload size={20} />
                            </ActionIcon>
                        )}
                        {metadata.children.length > 0 && (
                            <ActionIcon
                                size="lg"
                                onClick={() => setExpanded(!expanded)}
                            >
                                {expanded ? (
                                    <MdExpandLess size={20} />
                                ) : (
                                    <MdExpandMore size={20} />
                                )}
                            </ActionIcon>
                        )}
                    </Group>
                </Group>
                <Collapse in={expanded}>
                    <Stack spacing="sm">
                        {metadata.children.map((childId) => (
                            <NoteNode id={childId} key={childId} />
                        ))}
                    </Stack>
                </Collapse>
            </Stack>
            <ExportModal exporting={exporting} setExporting={setExporting} />
        </Paper>
    ) : (
        <Skeleton height={128} radius="sm" />
    );
}
