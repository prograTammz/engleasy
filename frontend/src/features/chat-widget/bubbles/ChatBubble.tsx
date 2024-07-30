import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
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

export const BotChatBubble: React.FC<BotChatBubbleProps> = ({
  botAvatar,
  botName,
  text,
}) => {
  return (
    <div className="flex gap-2 mb-4">
      <Avatar>
        <AvatarImage src={botAvatar} alt={botName} />
        <AvatarFallback>{botName}</AvatarFallback>
      </Avatar>
      <div className="bg-gray-200 dark:bg-gray-700 p-3 rounded-3xl rounded-tl-none">
        {text}
      </div>
    </div>
  );
};

export const UserChatBubble: React.FC<UserChatBubbleProps> = ({ text }) => {
  return (
    <div className="flex justify-end gap-2 mb-4">
      <div className="bg-purple-600 dark:bg-purple-200 p-3 rounded-3xl rounded-tr-none text-white dark:text-black">
        {text}
      </div>
    </div>
  );
};
