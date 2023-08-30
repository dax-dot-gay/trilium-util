import {
    ActionIcon,
    Collapse,
    ColorSwatch,
    Group,
    Paper,
    SimpleGrid,
    Stack,
    Text,
} from "@mantine/core";
import { useTriliumStatus } from "./util";
import { useDisclosure } from "@mantine/hooks";
import {
    MdAccessTime,
    MdAttachment,
    MdBuild,
    MdCalendarToday,
    MdDataArray,
    MdFolder,
    MdInfo,
    MdInfoOutline,
    MdListAlt,
    MdOpenInNew,
    MdSync,
} from "react-icons/md";
import { ReactNode, useMemo } from "react";

function StatusStatistic({
    name,
    value,
    icon,
}: {
    name: string;
    value: any;
    icon: ReactNode;
}) {
    return (
        <Stack p="xs" spacing={2}>
            <Group
                spacing="xs"
                style={{ pointerEvents: "none", userSelect: "none" }}
            >
                {icon}
                <Text fw={500}>{name}</Text>
            </Group>
            <Text color="dimmed">{value}</Text>
        </Stack>
    );
}

export function ServerStatus() {
    const status = useTriliumStatus();
    const [open, { toggle }] = useDisclosure(false);

    const currentUtc = useMemo(
        () =>
            status.online ? new Date(status.utcDateTime).toLocaleString() : "",
        [status]
    );

    return (
        <Paper radius="sm" p="sm">
            <Stack spacing="md">
                <Group position="apart">
                    <Group spacing="sm">
                        <ColorSwatch
                            color={status.online ? "green" : "red"}
                            size={24}
                        />
                        <Stack spacing={0} justify="left">
                            <Text size={18}>Server Status</Text>
                            <Group
                                spacing={2}
                                style={{ cursor: "pointer" }}
                                onClick={() =>
                                    window.open(status.url, "_blank")
                                }
                            >
                                <MdOpenInNew size={12} />
                                <Text size={12} italic color="dimmed">
                                    {status.url}
                                </Text>
                            </Group>
                        </Stack>
                    </Group>
                    <ActionIcon
                        onClick={toggle}
                        size="lg"
                        disabled={!status.online}
                        radius="xl"
                    >
                        {open ? (
                            <MdInfo size={24} />
                        ) : (
                            <MdInfoOutline size={24} />
                        )}
                    </ActionIcon>
                </Group>
                <Collapse in={open && status.online}>
                    {status.online && (
                        <SimpleGrid cols={4}>
                            <StatusStatistic
                                name="App Version"
                                value={status.appVersion}
                                icon={<MdListAlt size={20} />}
                            />
                            <StatusStatistic
                                name="DB Version"
                                value={status.dbVersion}
                                icon={<MdDataArray size={20} />}
                            />
                            <StatusStatistic
                                name="Sync Version"
                                value={status.syncVersion}
                                icon={<MdSync size={20} />}
                            />
                            <StatusStatistic
                                name="Clipper Version"
                                value={status.clipperProtocolVersion}
                                icon={<MdAttachment size={20} />}
                            />
                            <StatusStatistic
                                name="Data Directory"
                                value={status.dataDirectory}
                                icon={<MdFolder size={20} />}
                            />
                            <StatusStatistic
                                name="UTC Date/Time"
                                value={currentUtc}
                                icon={<MdAccessTime size={20} />}
                            />
                            <StatusStatistic
                                name="Build Revision"
                                value={status.buildRevision}
                                icon={<MdBuild size={20} />}
                            />
                            <StatusStatistic
                                name="Build Date"
                                value={new Date(
                                    status.buildDate
                                ).toLocaleString()}
                                icon={<MdCalendarToday size={20} />}
                            />
                        </SimpleGrid>
                    )}
                </Collapse>
            </Stack>
        </Paper>
    );
}
