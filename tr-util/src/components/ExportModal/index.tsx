import { useForm } from "@mantine/form";
import { useApiFunctions } from "../../hooks/api";
import {
    FileTypes,
    Note,
    NoteTypeExportable,
    fileTypesFeatures,
} from "../../types/note";
import {
    Button,
    Checkbox,
    Divider,
    Group,
    Modal,
    Stack,
    Switch,
    TextInput,
} from "@mantine/core";
import { useEffect, useState } from "react";
import { MdCloudDownload, MdEdit, MdError } from "react-icons/md";
import { notifications } from "@mantine/notifications";

export function ExportModal({
    exporting,
    setExporting,
}: {
    exporting: Note | null;
    setExporting: (id: Note | null) => void;
}) {
    const { post } = useApiFunctions();
    const [loading, setLoading] = useState(false);
    const form = useForm<{
        title: string;
        exportChildren: boolean;
        exportRelations: boolean;
        noteTypes: NoteTypeExportable[];
        fileExtensions: FileTypes[];
    }>({
        initialValues: {
            title: "New Export",
            exportChildren: true,
            exportRelations: true,
            noteTypes: ["text", "book", "canvas", "code"],
            fileExtensions: ["image", "plaintext"],
        },
    });

    useEffect(() => {
        form.reset();
    }, [exporting?.id]);

    return (
        <Modal
            opened={Boolean(exporting)}
            onClose={() => setExporting(null)}
            title={exporting ? `Export: ${exporting.title}` : ""}
        >
            <form
                onSubmit={form.onSubmit((values) => {
                    setLoading(true);
                    post<{ id: string }>(`/notes/${exporting?.id}/export`, {
                        data: {
                            id: exporting?.id,
                            title: values.title,
                            exportChildren: values.exportChildren,
                            exportRelations: values.exportRelations,
                            noteTypes: values.noteTypes,
                            fileTypes: values.fileExtensions,
                            mimeTypeMapping: fileTypesFeatures,
                        },
                    }).then((result) => {
                        setLoading(false);
                        if (result.success) {
                            window.open(
                                `/api/notes/exports/${result.value.id}`,
                                "_blank"
                            );
                            setExporting(null);
                        } else {
                            notifications.show({
                                color: "red",
                                icon: <MdError size={24} />,
                                message: "Failed to export note.",
                            });
                        }
                    });
                })}
            >
                <Stack spacing="sm">
                    <TextInput
                        label="Export Title"
                        icon={<MdEdit size={16} />}
                        {...form.getInputProps("title")}
                    />
                    <Switch
                        label="Export Children"
                        description="Export direct children of this note."
                        {...form.getInputProps("exportChildren", {
                            type: "checkbox",
                        })}
                    />
                    <Switch
                        label="Export Relations"
                        description="Export linked relations of this note."
                        {...form.getInputProps("exportRelations", {
                            type: "checkbox",
                        })}
                    />
                    <Divider />
                    <Checkbox.Group
                        {...form.getInputProps("noteTypes")}
                        label="Note Types"
                    >
                        <Stack spacing="xs">
                            <Checkbox value="text" label="Text Note" />
                            <Checkbox value="book" label="Book/Collection" />
                            <Checkbox value="code" label="Code Note" />
                            <Checkbox value="mermaid" label="Mermaid Diagram" />
                            <Checkbox value="canvas" label="Canvas Drawing" />
                            <Checkbox value="image" label="Image File" />
                            <Checkbox value="file" label="File" />
                        </Stack>
                    </Checkbox.Group>
                    <Divider />
                    <Checkbox.Group
                        {...form.getInputProps("fileExtensions")}
                        label="File Types"
                    >
                        <Stack spacing="xs">
                            <Checkbox value="plaintext" label="Plain Text" />
                            <Checkbox value="image" label="Images" />
                            <Checkbox value="html" label="HTML" />
                        </Stack>
                    </Checkbox.Group>
                    <Group position="right">
                        <Button
                            leftIcon={<MdCloudDownload size={20} />}
                            type="submit"
                            loading={loading}
                            disabled={loading}
                        >
                            Export
                        </Button>
                    </Group>
                </Stack>
            </form>
        </Modal>
    );
}
