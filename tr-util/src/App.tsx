import {
    AppShell,
    Button,
    Group,
    Header,
    MantineProvider,
    Title,
} from "@mantine/core";
import { MdLogin } from "react-icons/md";
import "./app.scss";

function App() {
    return (
        <MantineProvider
            withGlobalStyles
            withNormalizeCSS
            theme={{
                colorScheme: "dark",
            }}
        >
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
                            <Button
                                leftIcon={<MdLogin size={20} />}
                                variant="subtle"
                            >
                                Log In
                            </Button>
                        </Group>
                    </Header>
                }
            >
                <></>
            </AppShell>
        </MantineProvider>
    );
}

export default App;
