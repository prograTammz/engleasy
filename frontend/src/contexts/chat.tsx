import React, { createContext, useReducer, useContext, useEffect } from "react";
import useSocket from "../hooks/useSocket";
import { useAuth } from "./auth";
import { ChatAction, ChatMessage, ChatState } from "@/models/chat";
import { UserToken } from "@/models/user";

const initialState: ChatState = {
  messages: [],
};

const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case "ADD_MESSAGE":
      return { ...state, messages: [...state.messages, action.payload] };
    case "EDIT_MESSAGE":
      return {
        ...state,
        messages: state.messages.map((msg) =>
          msg.id === action.payload.id
            ? {
                ...msg,
                text: action.payload.text,
                is_modified: true,
                modified: new Date().toISOString(),
              }
            : msg
        ),
      };
    case "DELETE_MESSAGE":
      return {
        ...state,
        messages: state.messages.filter((msg) => msg.id !== action.payload),
      };
    case "SET_MESSAGES":
      return { ...state, messages: action.payload };
    default:
      return state;
  }
};

const ChatContext = createContext<{
  messages: ChatMessage[];
  sendMessage: (message: ChatMessage) => void;
  editMessage: (id: string, text: string) => void;
  deleteMessage: (id: string) => void;
} | null>(null);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { userToken } = useAuth();
  const { messages: socketMessages, sendMessage: socketSendMessage } =
    useSocket("ws://your-websocket-url/ws", userToken as UserToken);
  const [{ messages }, dispatch] = useReducer(chatReducer, initialState);

  useEffect(() => {
    dispatch({ type: "SET_MESSAGES", payload: socketMessages });
  }, [socketMessages]);

  const setMessages = () => {
    //To be implemented
  };

  const sendMessage = (message: ChatMessage) => {
    socketSendMessage(message);
    dispatch({ type: "ADD_MESSAGE", payload: message });
  };

  const editMessage = (id: string, text: string) => {
    dispatch({ type: "EDIT_MESSAGE", payload: { id, text } });
    // Add logic to update message on the server if needed
  };

  const deleteMessage = (id: string) => {
    dispatch({ type: "DELETE_MESSAGE", payload: id });
    // Add logic to delete message on the server if needed
  };

  return (
    <ChatContext.Provider
      value={{ messages, sendMessage, editMessage, deleteMessage }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
};
