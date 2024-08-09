import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import React from "react";
import { BotAvatar } from "./BotAvatar";
import { VoiceRecorder } from "./VoiceRecorder";
import { MessageBox } from "./MessageBox";

export const MessageArea: React.FC = () => {
  return (
    <Tabs defaultValue="text" className="w-full">
      <TabsList className="flex w-full">
        <TabsTrigger
          value="text"
          className="flex-grow data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow data-[state=inactive]:bg-muted"
        >
          Text
        </TabsTrigger>
        <TabsTrigger
          value="audio"
          className="flex-grow data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow data-[state=inactive]:bg-muted"
        >
          Audio
        </TabsTrigger>
      </TabsList>
      <TabsContent value="text">
        <div className="flex flex-col w-full gap-4">
          <div className="flex w-full">
            <BotAvatar />
            <MessageBox />
          </div>
        </div>
      </TabsContent>
      <TabsContent value="audio">
        <VoiceRecorder />
      </TabsContent>
    </Tabs>
  );
};
