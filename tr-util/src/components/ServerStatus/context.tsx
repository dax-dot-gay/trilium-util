import { ReactNode, useEffect, useState } from "react";
import { useApiFeatures, useApiFunctions } from "../../hooks/api";
import { TriliumStatus } from "../../types/trilium";
import { TriliumStatusContext } from "./util";

export function TriliumStatusProvider({
    children,
}: {
    children?: ReactNode | ReactNode[];
}) {
    const { loggedIn, unauthenticatedViewing } = useApiFeatures();
    const [status, setStatus] = useState<TriliumStatus>({
        online: false,
        url: "",
    });
    const { get } = useApiFunctions();

    useEffect(() => {
        function getStatus() {
            get<TriliumStatus>("/notes/status").then((result) =>
                result.success
                    ? setStatus(result.value)
                    : console.warn("Failure to fetch status: " + result.reason)
            );
        }
        getStatus();
        const interval = setInterval(getStatus, 5000);
        return () => clearInterval(interval);
    }, [loggedIn, unauthenticatedViewing]);
    return (
        <TriliumStatusContext.Provider value={status}>
            {children}
        </TriliumStatusContext.Provider>
    );
}
