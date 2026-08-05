import { apiRequest, setTokens, clearTokens } from "./api";

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface UserResponse {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  channel: string;
  subscribers: number;
}

export async function signup(name: string, email: string, password: string): Promise<TokenResponse> {
  const data = await apiRequest<TokenResponse>("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ name, email, password }),
  });
  setTokens(data.access_token, data.refresh_token);
  return data;
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const data = await apiRequest<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  setTokens(data.access_token, data.refresh_token);
  return data;
}

export async function logout(): Promise<void> {
  await apiRequest("/auth/logout", { method: "POST" });
  clearTokens();
}

export async function getMe(): Promise<UserResponse> {
  return apiRequest<UserResponse>("/me");
}

export async function updateProfile(data: { name?: string; channel?: string; niche?: string }): Promise<UserResponse> {
  return apiRequest<UserResponse>("/profile", {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function forgotPassword(email: string): Promise<{ message: string }> {
  return apiRequest("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function completeOnboarding(data: {
  creatorType: string;
  platforms: string[];
  goals: string[];
  niche: string;
  theme: string;
}): Promise<{ message: string }> {
  return apiRequest("/onboarding", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
