import React from "react";

interface ChatBubbleProps {
  text: string;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ text }) => {
  return <div>{text}</div>;
};
