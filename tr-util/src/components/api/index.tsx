import { ReactNode, useEffect, useState } from "react";
import { ApiContext, ApiResponse } from "./typing";
import { AuthRequired, Session } from "../../types/auth";

export function ApiProvider({
    children,
}: {
    children?: ReactNode | ReactNode[];
}) {
    const [token, setToken] = useState<string | null>(
        localStorage.getItem("token")
    );

    const [loggedIn, setLoggedIn] = useState<boolean>(false);
    const [unauthenticatedViewing, setUnauthenticatedViewing] =
        useState<boolean>(false);

    async function request<T = any>(
        method: "GET" | "POST" | "DELETE",
        url: string,
        options?: {
            params?: { [key: string]: string };
            data?: any;
        }
    ): Promise<ApiResponse<T>> {
        const rawResult = await fetch(
            "/api" +
                url +
                (options?.params
                    ? "?" + new URLSearchParams(options.params)
                    : ""),
            {
                method,
                body: options?.data ? JSON.stringify(options.data) : undefined,
                headers: {
                    Authorization: token ?? "null",
                    "Content-Type": "application/json",
                },
            }
        );

        if (rawResult.status === 204) {
            return {
                success: true,
                value: null as T,
            };
        }

        const resultText = await rawResult.text();

        if (rawResult.ok) {
            try {
                return {
                    success: true,
                    value: JSON.parse(resultText),
                };
            } catch {
                return {
                    success: true,
                    value: resultText as T,
                };
            }
        } else {
            return {
                success: false,
                code: rawResult.status,
                reason: resultText,
            };
        }
    }

    useEffect(() => {
        request<Session>("GET", "/auth").then((result) => {
            if (result.success) {
                setToken(result.value.token);
                setLoggedIn(result.value.logged_in);
                localStorage.setItem("token", result.value.token);
            }
        });
    }, []);

    useEffect(() => {
        request<AuthRequired>("GET", "/auth/required").then((result) => {
            if (result.success) {
                setUnauthenticatedViewing(result.value.required);
            }
        });
    }, []);

    return (
        <ApiContext.Provider
            value={{
                get: async function <T>(
                    url: string,
                    options?: { params?: { [key: string]: string } }
                ) {
                    return await request<T>("GET", url, options);
                },
                del: async function <T>(
                    url: string,
                    options?: { params?: { [key: string]: string } }
                ) {
                    return await request<T>("DELETE", url, options);
                },
                post: async function <T>(
                    url: string,
                    options?: { params?: { [key: string]: string }; data?: any }
                ) {
                    return await request<T>("POST", url, options);
                },
                features: {
                    loggedIn,
                    unauthenticatedViewing,
                },
                utilities: {
                    login: async (password: string) => {
                        const result = await request<Session>(
                            "POST",
                            "/auth/login",
                            {
                                data: {
                                    password,
                                },
                            }
                        );
                        return result.success ? result.value : null;
                    },
                    logout: async () => {
                        const result = await request<Session>(
                            "POST",
                            "/auth/logout"
                        );
                        return result.success
                            ? result.value
                            : { token: token ?? "", logged_in: loggedIn };
                    },
                },
            }}
        >
            {children}
        </ApiContext.Provider>
    );
}
