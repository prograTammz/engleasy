import React, { createContext, useReducer, useContext } from "react";
import useStorage from "@/hooks/useStorage";
import { User, UserToken } from "@/models/user";
import { Action, ContextValue, State } from "@/models/auth";
import AuthAPI from "@/services/apiAuth";
import { useToast } from "@/components/ui/use-toast";
import { useNavigate } from "react-router-dom";

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
  const navigate = useNavigate();
  const { toast } = useToast();

  const login = async (email: string, password: string) => {
    const user: User = { email, password };
    try {
      const userToken = await AuthAPI.login(user);
      setItem(userToken);
      navigate("/app");
      toast({
        title: "Successful!",
        description: <span>You are logged in!</span>,
      });
      dispatch({ type: "LOGIN", payload: { userToken } });
    } catch (error: unknown) {
      // Handler Error Show a toast
      const message = (error as Error).message;
      toast({
        title: "Authentication Error",
        description: <span>{message}</span>,
        variant: "destructive",
      });
    }
  };

  const logout = () => {
    removeItem();
    dispatch({ type: "LOGOUT" });
  };

  const register = async (email: string, name: string, password: string) => {
    const userPayload: User = { email, name, password };
    try {
      const userResponse = await AuthAPI.register(userPayload);
      dispatch({ type: "REGISTER", payload: { user: userResponse } });
      navigate("/login");
      toast({
        title: "Successful!",
        description: <span>You account has been created Successfully!</span>,
      });
    } catch (error: unknown) {
      const message = (error as Error).message;
      toast({
        title: "Authentication Error",
        description: <span>{message}</span>,
        variant: "destructive",
      });
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, userToken, isAuthenticated, login, logout, register }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
