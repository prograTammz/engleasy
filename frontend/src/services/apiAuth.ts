import { User, UserToken } from "@/models/user";

const API_URL = "http://localhost:8000/auth";

async function login(user: User): Promise<UserToken> {
  try {
    const res = await fetch(`${API_URL}/token`, {
      body: JSON.stringify(user),
      headers: {
        "Content-Type": "application/json",
      },
    });
    return await res.json();
  } catch {
    throw new Error("Authentication has failed successfully!");
  }
}

async function register(user: User): Promise<User> {
  try {
    const res = await fetch(`${API_URL}/token`, {
      body: JSON.stringify(user),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return await res.json();
  } catch {
    throw new Error("Authentication has failed successfully!");
  }
}

export default { login, register };
