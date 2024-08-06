export interface UserToken {
  access_token: string;
  token_type: string;
}

export interface User {
  id?: string;
  name?: string;
  email: string;
  password?: string;
}
