import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "@/components/ui/context-menu";
import { ChatMessage, ChatSender } from "@/models/chat";

import React from "react";

type BaseBubbleProps = {
  chatMessage: ChatMessage;
  children: React.ReactNode;
};

export const BaseBubble: React.FC<BaseBubbleProps> = ({
  chatMessage,
  children,
}) => {
  const handleEdit = () => {
    // TODO: handle Edit
    console.log("Edit is working");
  };

  const handleDelete = () => {
    // TODO: handle delete
    console.log("Delete is working");
  };

  return (
    <ContextMenu>
      <ContextMenuTrigger>
        <div
          className={`flex flex-col ${
            chatMessage.sender === ChatSender.USER && "items-end"
          } my-2`}
        >
          <div className={`flex gap-2 mb-2`}>
            {chatMessage.sender === ChatSender.BOT && (
              <Avatar>
                <AvatarImage
                  src="https://api.dicebear.com/9.x/micah/svg?seed=Boo"
                  alt="Ava"
                />
                <AvatarFallback>Ava</AvatarFallback>
              </Avatar>
            )}

            {chatMessage.sender === ChatSender.BOT ? (
              <div className="bg-gray-200 dark:bg-gray-700 p-3 rounded-3xl rounded-tl-none">
                {children}
              </div>
            ) : (
              <div className="bg-purple-600 dark:bg-purple-200 p-3 rounded-3xl rounded-tr-none text-white dark:text-black">
                {children}
              </div>
            )}
          </div>

          <span className="text-xs text-muted-foreground ">
            {chatMessage.is_modified
              ? `Edited at ${formatDate(chatMessage.modified)}`
              : `Sent at ${formatDate(chatMessage.created)}`}
          </span>
        </div>
      </ContextMenuTrigger>
      <ContextMenuContent>
        <ContextMenuItem onClick={() => handleEdit()}>Edit</ContextMenuItem>
        <ContextMenuItem onClick={() => handleDelete()}>Delete</ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
};

function formatDate(date: Date): string {
  date = new Date(date);
  console.log(date);
  const day = date.getDay();
  const month = date.getMonth();
  const year = date.getFullYear();
  // Time
  const hour = date.getHours();
  const minute = date.getMinutes();

  return `${month}/${day}/${year} ${hour}:${minute}`;
}
