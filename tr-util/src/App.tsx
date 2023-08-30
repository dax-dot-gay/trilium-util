import {
    MantineProvider,
} from "@mantine/core";
import "./app.scss";
import { ApiProvider } from "./components/api";
import { ApplicationShell } from "./components/shell/ApplicationShell";
import { Notifications } from "@mantine/notifications";

function App() {
    return (
        <ApiProvider>
            <MantineProvider
                withGlobalStyles
                withNormalizeCSS
                theme={{
                    colorScheme: "dark",
                    globalStyles(theme) {
                        return {
                            body: {
                                backgroundColor: theme.colors.dark[8],
                            },
                        };
                    },
                }}
            >
                <Notifications />
                <ApplicationShell />
            </MantineProvider>
        </ApiProvider>
    );
}

export default App;
