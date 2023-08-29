import { MantineProvider } from "@mantine/core";

function App() {
    return (
        <MantineProvider
            withGlobalStyles
            withNormalizeCSS
            theme={{
                colorScheme: "dark",
            }}
        >
            <></>
        </MantineProvider>
    );
}

export default App;
