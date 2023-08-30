import { Button, Group, Modal, PasswordInput, Stack } from "@mantine/core";
import { useApiUtilities } from "../../hooks/api";
import {
    MdCheck,
    MdError,
    MdLock,
    MdVisibility,
    MdVisibilityOff,
} from "react-icons/md";
import { useEffect, useState } from "react";
import { notifications } from "@mantine/notifications";

export function LoginModal({
    open,
    setOpen,
}: {
    open: boolean;
    setOpen: (open: boolean) => void;
}) {
    const { login } = useApiUtilities();
    const [password, setPassword] = useState<string>("");
    useEffect(() => {
        setPassword("");
    }, [open]);
    return (
        <Modal
            w="md"
            withCloseButton
            title="Log In"
            opened={open}
            onClose={() => setOpen(false)}
            centered
        >
            <Stack spacing="sm">
                <PasswordInput
                    visibilityToggleIcon={({ reveal, size }) =>
                        reveal ? (
                            <MdVisibilityOff size={size} />
                        ) : (
                            <MdVisibility size={size} />
                        )
                    }
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    label="Password"
                    icon={<MdLock size={16} />}
                />
                <Group position="right">
                    <Button
                        leftIcon={<MdCheck size={16} />}
                        onClick={() => {
                            login(password).then((result) => {
                                if (result) {
                                    notifications.show({
                                        color: "green",
                                        icon: <MdCheck size={24} />,
                                        message: "Login successful!",
                                    });
                                    setOpen(false);
                                } else {
                                    notifications.show({
                                        color: "red",
                                        icon: <MdError size={24} />,
                                        message: "Failed to login.",
                                    });
                                    setPassword("");
                                }
                            });
                        }}
                    >
                        Log In
                    </Button>
                </Group>
            </Stack>
        </Modal>
    );
}
