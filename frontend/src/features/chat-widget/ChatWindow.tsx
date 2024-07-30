import React, { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Cross2Icon, PaperPlaneIcon, PlayIcon } from "@radix-ui/react-icons";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { BotChatBubble, UserChatBubble } from "./bubbles/ChatBubble";
import { PhaseBubble } from "./bubbles/PhaseBubble";
import { Tabs } from "@/components/ui/tabs";
import { TabsContent, TabsList, TabsTrigger } from "@radix-ui/react-tabs";
import AudioRecorder from "./AudioRecorder";

export const ChatWindow: React.FC = () => {
  const [open, setOpen] = useState<boolean>(false);
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="secondary"> Open</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <div className="flex justify-end w-full">
            <Button variant="outline" size="icon" className="p-0">
              <Cross2Icon className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex justify-center">
            <div className="flex flex-col items-center gap-2">
              <Avatar>
                <AvatarImage
                  src="https://api.dicebear.com/9.x/micah/svg?seed=Boo"
                  alt="@Ava"
                />
                <AvatarFallback>Ava</AvatarFallback>
              </Avatar>
              <h2 className="font-bold">Hey 👋 I'm Ava</h2>
              <p className="text-gray-500">
                Ask me anything or pick a place to start
              </p>
            </div>
          </div>
        </DialogHeader>
        {/* Body */}
        <ScrollArea className="h-[400px] w-full">
          <BotChatBubble
            text="Hi Jane, Amazing how mosey is similificng state complicance!"
            botAvatar="https://api.dicebear.com/9.x/micah/svg?seed=Boo"
            botName="Ava"
            isLoading={false}
          />
          <UserChatBubble text="Hi, thanks for connecting" />
          <PhaseBubble phaseName="Listening" phaseNumber={1} />
        </ScrollArea>

        {/* This is the footer */}
        <Separator />
        <DialogFooter>
          <Tabs defaultValue="text" className="w-full">
            <TabsList className="items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground grid w-full grid-cols-2 mb-4">
              <TabsTrigger
                value="text"
                className="inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow data-[state=inactive]:bg-muted"
              >
                Text
              </TabsTrigger>
              <TabsTrigger
                value="audio"
                className="inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow data-[state=inactive]:bg-muted"
              >
                Audio
              </TabsTrigger>
            </TabsList>
            <TabsContent value="text">
              <div className="flex flex-col w-full gap-4">
                <div className="flex w-full">
                  <Avatar>
                    <AvatarImage
                      src="https://api.dicebear.com/9.x/micah/svg?seed=Oliver"
                      alt="@Ava"
                    />
                    <AvatarFallback>Ava</AvatarFallback>
                  </Avatar>
                  <Textarea className="w-full" />
                </div>
                <div className="flex justify-end gap-2">
                  <Button variant="outline" size="icon" className="p-0">
                    <PlayIcon />
                    <span className="sr-only">Record a voice message</span>
                  </Button>
                  <Button variant="secondary" size="icon" className="p-0">
                    <PaperPlaneIcon />
                    <span className="sr-only">Send Message</span>
                  </Button>
                </div>
              </div>
            </TabsContent>
            <TabsContent value="audio"></TabsContent>
          </Tabs>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
