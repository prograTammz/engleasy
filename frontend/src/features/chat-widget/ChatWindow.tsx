import React from "react";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export const ChatWindow: React.FC = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="secondary"> Open</Button>
      </DialogTrigger>
      <DialogContent>
        {/* Header */}
        <DialogHeader>This is the header</DialogHeader>
        {/* Body */}
        <div className="grid gap-4 py-4">this is the body</div>
        {/* This is the footer */}
        <DialogFooter>Footer</DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
