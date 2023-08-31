import { createContext, useContext } from "react";
import { Session } from "../../types/auth";

export type ApiResponse<T = any> =
    | {
          success: true;
          value: T;
      }
    | {
          success: false;
          code: number;
          reason: string;
      };

export type ApiContextType = {
    get: <T = any>(
        url: string,
        options?: { params?: { [key: string]: string } }
    ) => Promise<ApiResponse<T>>;
    post: <T = any>(
        url: string,
        options?: { params?: { [key: string]: string }; data?: any }
    ) => Promise<ApiResponse<T>>;
    del: <T = any>(
        url: string,
        options?: { params?: { [key: string]: string } }
    ) => Promise<ApiResponse<T>>;
    features: {
        loggedIn: boolean;
        unauthenticatedViewing: boolean;
    };
    utilities: {
        login: (password: string) => Promise<Session | null>;
        logout: () => Promise<Session>;
    };
};

export const ApiContext = createContext<ApiContextType>(null as any);
