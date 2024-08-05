import { User, UserToken } from "@/models/user";
import { ReactNode } from "react";

export interface State {
  isAuthenticated: boolean;
  userToken: UserToken | null;
  user: User | null;
}

export interface ContextValue extends State {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, name: string, password: string) => Promise<void>;
}

// Define the AuthProviderProps interface for specifying props of AuthProvider
export interface AuthProviderProps {
  children: ReactNode;
}

export type LoginAction = {
  type: "LOGIN";
  payload: {
    userToken: UserToken;
  };
};

export type LogoutAction = {
  type: "LOGOUT";
};

export type RegisterAction = {
  type: "REGISTER";
  payload: {
    user: User;
  };
};

export type Action = LoginAction | LogoutAction | RegisterAction;
