import React, { createContext, useReducer, useContext } from "react";
import useStorage from "@/hooks/useStorage";
import { User, UserToken } from "@/models/user";
import { Action, ContextValue, State } from "@/models/auth";
import AuthAPI from "@/services/apiAuth";

const initialState: State = {
  userToken: null,
  user: null,
  isAuthenticated: false,
};

const AuthContext = createContext<ContextValue>({
  ...initialState,
  login: () => Promise.resolve(),
  logout: () => Promise.resolve(),
  register: () => Promise.resolve(),
});

const authReducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "LOGIN":
      return {
        ...state,
        userToken: action.payload.userToken,
        isAuthenticated: true,
      };
    case "LOGOUT":
      return { ...state, userToken: null, isAuthenticated: false };
    case "REGISTER":
      return { ...state, userToken: null, isAuthenticated: false };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { setItem, removeItem } = useStorage<UserToken>("authToken");
  const [{ user, userToken, isAuthenticated }, dispatch] = useReducer(
    authReducer,
    initialState
  );

  const login = async (email: string, password: string) => {
    const user: User = { email, password };
    const userToken = await AuthAPI.login(user);
    setItem(userToken);
    dispatch({ type: "LOGIN", payload: { userToken } });
  };

  const logout = () => {
    removeItem();
    dispatch({ type: "LOGOUT" });
  };

  const register = async () => {};

  return (
    <AuthContext.Provider
      value={{ user, userToken, isAuthenticated, login, logout, register }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
