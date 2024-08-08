export enum ChatType {
  TEXT = "text",
  AUDIO = "audio",
  SHEET = "sheet",
}

export enum ChatSender {
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

export interface ChatState {
  messages: ChatMessage[];
}

export type ChatAction =
  | { type: "ADD_MESSAGE"; payload: ChatMessage }
  | { type: "EDIT_MESSAGE"; payload: { id: string; text: string } }
  | { type: "DELETE_MESSAGE"; payload: string }
  | { type: "SET_MESSAGES"; payload: ChatMessage[] };
