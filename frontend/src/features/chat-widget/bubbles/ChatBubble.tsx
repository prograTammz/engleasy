import React from "react";

interface BotChatBubbleProps {
  botAvatar: string;
  botName: string;
  text: string;
  isLoading: boolean;
}

interface UserChatBubbleProps {
  text: string;
}

export const BotChatBubble: React.FC<BotChatBubbleProps> = ({ text }) => {
  return <div>{text}</div>;
};

export const UserChatBubble: React.FC<UserChatBubbleProps> = ({ text }) => {
  return <div>{text}</div>;
};
