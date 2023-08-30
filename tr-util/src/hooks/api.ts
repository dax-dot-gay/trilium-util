import { useContext } from "react";
import { ApiContext, ApiContextType } from "../components/api/typing";

export function useApi(): ApiContextType {
    return useContext(ApiContext);
}

export function useApiFunctions(): Omit<ApiContextType, "features" | "utilities"> {
    const {get, post, del} = useApi();
    return {get, post, del};
}

export function useApiFeatures(): ApiContextType["features"] {
    return useApi().features;
}

export function useApiUtilities(): ApiContextType["utilities"] {
    return useApi().utilities;
}