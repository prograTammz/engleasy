import { useEffect, useState } from "react";
import { UserToken } from "@/models/user";
import { ChatMessage } from "@/models/chat";

const useSocket = (url: string, userToken: UserToken) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socket.onopen = () => {
      socket.send(
        JSON.stringify({ type: "auth", token: userToken.access_token })
      );
    };

    socket.onmessage = (event) => {
      const message: ChatMessage = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    socket.onclose = () => {
      console.log("WebSocket closed");
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, [url, userToken]);

  const sendMessage = (message: ChatMessage) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  };

  return { messages, sendMessage };
};

export default useSocket;
