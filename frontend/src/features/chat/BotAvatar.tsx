import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import React from "react";

export const BotAvatar: React.FC = () => {
  return (
    <Avatar>
      <AvatarImage
        src="https://api.dicebear.com/9.x/micah/svg?seed=Oliver"
        alt="@Ava"
      />
      <AvatarFallback>Ava</AvatarFallback>
    </Avatar>
  );
};
