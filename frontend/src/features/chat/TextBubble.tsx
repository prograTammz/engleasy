import { ChatMessage } from "@/models/chat";
import { BaseBubble } from "./BaseBubble";

type TextBubbleProps = {
  chatMessage: ChatMessage;
};

export const TextBubble: React.FC<TextBubbleProps> = ({ chatMessage }) => {
  return (
    <BaseBubble chatMessage={chatMessage}>
      <span>{chatMessage.content}</span>
    </BaseBubble>
  );
};
