// Authentication types based on our FastAPI backend

export interface UserSignupRequest {
  email: string;
  password: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
}

export interface UserResponse {
  id: string;
  email: string;
  message: string;
}

export interface PasswordResetRequest {
  email: string;
}

export interface ApiError {
  detail: string;
} 