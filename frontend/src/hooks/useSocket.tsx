import { useEffect, useState } from "react";
import { UserToken } from "@/models/user";
import { ChatMessage, ChatType } from "@/models/chat";

const useSocket = (url: string, userToken: UserToken) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [socket, setSocket] = useState<WebSocket | null>();

  useEffect(() => {
    if (socket) {
      socket.onopen = () => {
        socket.send(
          JSON.stringify({ type: "auth", token: userToken.access_token })
        );
      };

      socket.onmessage = (event) => {
        const message: ChatMessage = JSON.parse(JSON.parse(event.data));
        console.log(message);
        setMessages((prevMessages) => [...prevMessages, message]);
      };

      socket.onclose = () => {
        console.log("WebSocket closed");
      };
    }

    // return () => {
    //   console.log("closed");
    //   closeSocket();
    // };
  }, [url, userToken, socket]);

  const openSocket = () => {
    const socket = new WebSocket(url);
    setSocket(socket);
  };

  const closeSocket = () => {
    socket?.close();
    setSocket(null);
  };

  const sendMessage = (message: ChatMessage) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      if (message.type === ChatType.TEXT) {
        socket.send(JSON.stringify(message.content));
      }
    }
  };

  return { messages, openSocket, sendMessage };
};

export default useSocket;
