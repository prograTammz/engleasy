import { User, UserToken } from "@/models/user";

const API_URL = "http://localhost:8000/auth";

async function login(user: User): Promise<UserToken> {
  try {
    const res = await fetch(`${API_URL}/login`, {
      body: JSON.stringify(user),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.status !== 200) {
      const body = await res.json();
      throw new Error(body?.detail);
    }
    return await res.json();
  } catch (error: unknown) {
    const message = (error as Error).message;
    throw new Error(message ?? "Authentication has failed successfully!");
  }
}

async function register(user: User): Promise<User> {
  try {
    const res = await fetch(`${API_URL}/register`, {
      body: JSON.stringify(user),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.status !== 201) {
      const body = await res.json();
      throw new Error(body?.detail);
    }
    return await res.json();
  } catch (error: unknown) {
    const message = (error as Error).message;
    throw new Error(message ?? "Register has failed successfully!");
  }
}

export default { login, register };
