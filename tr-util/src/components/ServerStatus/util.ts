import { createContext, useContext } from "react";
import { TriliumStatus } from "../../types/trilium";

export const TriliumStatusContext = createContext<TriliumStatus>({online: false, url: ""});

export function useTriliumStatus(): TriliumStatus {
    return useContext(TriliumStatusContext);
}