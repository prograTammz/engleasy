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
import { Cross2Icon } from "@radix-ui/react-icons";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";

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
            <Button variant="ghost" size="icon">
              <Cross2Icon className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex justify-center">
            <div className="flex flex-col items-center gap-2">
              <Avatar>
                <AvatarImage
                  src="https://api.dicebear.com/9.x/micah/svg"
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
          <div className="grid gap-4 py-4">this is the body</div>
        </ScrollArea>

        {/* This is the footer */}
        <Separator />
        <DialogFooter></DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
