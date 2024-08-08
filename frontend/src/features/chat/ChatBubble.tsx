import { ChatMessage, ChatSender, ChatType } from "@/models/chat";
import React from "react";
import { TextBubble } from "./TextBubble";
import { AudioBubble } from "./AudioBubble";
import { SheetBubble } from "./SheetBubble";
import { EnglishScoreSheet } from "@/models/score";
import { LoadingBubble } from "./LoadingBubble";

type BaseBubbleProps = {
  chatMessage?: ChatMessage;
  chatSender?: ChatSender;
  isLoading?: boolean;
};

export const ChatBubble: React.FC<BaseBubbleProps> = ({
  chatMessage,
  chatSender = ChatSender.BOT,
  isLoading = false,
}) => {
  if (isLoading && chatSender) {
    return <LoadingBubble chatSender={chatSender} />;
  }

  if (chatMessage === null) {
    return;
  }

  return (
    <>
      {chatMessage!.type === ChatType.TEXT && (
        <TextBubble chatMessage={chatMessage!} />
      )}
      {chatMessage!.type === ChatType.AUDIO && (
        <AudioBubble chatMessage={chatMessage!} />
      )}
      {chatMessage!.type === ChatType.SHEET && (
        <SheetBubble
          score_sheet={JSON.parse(chatMessage!.content)}
          chatMessage={chatMessage!}
        />
      )}
    </>
  );
};
