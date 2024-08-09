import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Cross2Icon, PaperPlaneIcon, PlayIcon } from "@radix-ui/react-icons";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { Tabs } from "@/components/ui/tabs";
import { TabsContent, TabsList, TabsTrigger } from "@radix-ui/react-tabs";
import { VoiceRecorder } from "../chat/VoiceRecorder";
import { ChatBubble } from "../chat/ChatBubble";
import { ChatSender, ChatType } from "@/models/chat";
import { exampleSheet } from "@/models/score";
import { useChat } from "@/contexts/chat";
import { MessageArea } from "../chat/MessageArea";
import { BotAvatar } from "../chat/BotAvatar";

export const ChatWindow: React.FC = () => {
  const { messages, initalizeChat } = useChat();

  useEffect(() => {
    initalizeChat();
    return () => {
      console.log("bye");
    };
  }, []);

  useEffect(() => () => console.log("unmount"), []);

  return (
    <div className="w-full h-full max-w-screen-md flex flex-col justify-between gap-4">
      <div className="flex justify-center">
        <div className="flex flex-col items-center gap-2">
          <BotAvatar />
          <h2 className="font-bold">Hey 👋 I'm Ava</h2>
          <p className="text-gray-500">
            Ask me anything or pick a place to start
          </p>
        </div>
      </div>
      {/* Body */}
      <ScrollArea className="h-[400px] w-full shadow-background shadow-inner bg-muted flex-grow px-2 rounded-lg">
        {messages &&
          messages.map((message) => {
            return <ChatBubble key={message.id} chatMessage={message} />;
          })}
      </ScrollArea>

      <MessageArea />
    </div>
  );
};
