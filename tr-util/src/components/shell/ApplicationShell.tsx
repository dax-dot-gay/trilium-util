import {
    AppShell,
    Header,
    Group,
    Title,
    Button,
    Paper,
    Stack,
    Text,
    Box,
} from "@mantine/core";
import { MdLogin, MdLogout } from "react-icons/md";
import { useApiFeatures, useApiUtilities } from "../../hooks/api";
import "./shell.scss";
import { LoginModal } from "../LoginModal";
import { useState } from "react";

export function ApplicationShell() {
    const { loggedIn, unauthenticatedViewing } = useApiFeatures();
    const [login, setLogin] = useState(false);
    const { logout } = useApiUtilities();
    return (
        <AppShell
            className="app"
            header={
                <Header p="xs" height={60} className="app-header">
                    <Group position="apart">
                        <Group spacing="sm" className="app-title">
                            <img
                                src="/icon.png"
                                alt="Application Logo"
                                className="app-logo"
                            />
                            <Title order={3}>Trilium Utilities</Title>
                        </Group>
                        {loggedIn ? (
                            <Button
                                leftIcon={<MdLogout size={20} />}
                                variant="subtle"
                                onClick={() => logout()}
                            >
                                Log Out
                            </Button>
                        ) : (
                            <Button
                                leftIcon={<MdLogin size={20} />}
                                variant="subtle"
                                onClick={() => setLogin(true)}
                            >
                                Log In
                            </Button>
                        )}
                    </Group>
                </Header>
            }
        >
            <Box className="application-content" p="sm">
                {loggedIn || unauthenticatedViewing ? (
                    <></>
                ) : (
                    <Paper p="lg" radius="sm" className="login-required">
                        <Stack spacing="lg" align="center" justify="center">
                            <Text color="dimmed" size={24}>
                                Login to access this service.
                            </Text>
                            <Button
                                leftIcon={<MdLogin size={20} />}
                                size="md"
                                onClick={() => setLogin(true)}
                            >
                                Log In
                            </Button>
                        </Stack>
                    </Paper>
                )}
            </Box>
            <LoginModal open={login} setOpen={setLogin} />
        </AppShell>
    );
}
