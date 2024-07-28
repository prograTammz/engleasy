import React from "react";

interface BotChatBubbleProps {
  botAvatar: string;
  botName: string;
  text: string;
  isLoading: boolean;
}

export const ChatBubble: React.FC<BotChatBubbleProps> = ({ text }) => {
  return <div>{text}</div>;
};
