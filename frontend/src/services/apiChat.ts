import { ChatHistory, ChatMessage } from "@/models/chat";
import { UserToken } from "@/models/user";

const API_URL = "http://localhost:8000/chat/messages";

export async function getMessages(userToken: UserToken): Promise<ChatHistory> {
  try {
    const res = await fetch(`${API_URL}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `${userToken.token_type} ${userToken.access_token}`,
      },
    });
    if (res.status !== 200) {
      const body = await res.json();
      throw new Error(body?.detail);
    }
    return await res.json();
  } catch (error: unknown) {
    const message = (error as Error).message;
    throw new Error(message ?? "Failed to fetch messages!");
  }
}

export async function editMessage(
  userToken: UserToken,
  messageId: string,
  newText: string
): Promise<ChatMessage> {
  try {
    const res = await fetch(`${API_URL}/${messageId}`, {
      method: "PUT",
      body: JSON.stringify({ text: newText }),
      headers: {
        "Content-Type": "application/json",
        Authorization: `${userToken.token_type} ${userToken.access_token}`,
      },
    });
    if (res.status !== 200) {
      const body = await res.json();
      throw new Error(body?.detail);
    }
    return await res.json();
  } catch (error: unknown) {
    const message = (error as Error).message;
    throw new Error(message ?? "Failed to edit message!");
  }
}

export async function deleteMessage(
  userToken: UserToken,
  messageId: string
): Promise<{ message: string }> {
  try {
    const res = await fetch(`${API_URL}/${messageId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `${userToken.token_type} ${userToken.access_token}`,
      },
    });
    if (res.status !== 200) {
      const body = await res.json();
      throw new Error(body?.detail);
    }
    return await res.json();
  } catch (error: unknown) {
    const message = (error as Error).message;
    throw new Error(message ?? "Failed to delete message!");
  }
}
