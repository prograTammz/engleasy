enum ChatType {
  TEXT = "text",
  AUDIO = "audio",
  SHEET = "sheet",
}

enum ChatSender {
  USER = "user",
  BOT = "bot",
}

export interface ChatMessage {
  id: string;
  content: string;
  type: ChatType;
  created: Date;
  modified: Date;
  is_modified: boolean;
  sender: ChatSender;
}
