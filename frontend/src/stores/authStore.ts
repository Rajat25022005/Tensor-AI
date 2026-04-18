import { create } from "zustand";
import { api } from "../services/api";
import type { LoginCredentials, User } from "../types";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => Promise<void>;
  checkSession: () => Promise<boolean>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  login: async (credentials: LoginCredentials) => {
    set({ isLoading: true, error: null });
    try {
      const res = await api.post("/auth/login", credentials);
      if (res.status === 200) {
        // Login sets httpOnly cookie. Now fetch user profile.
        const meRes = await api.get("/auth/me");
        set({ 
          user: meRes.data as User, 
          isAuthenticated: true, 
          isLoading: false 
        });
        return true;
      }
      set({ error: "Login failed", isLoading: false });
      return false;
    } catch (err: any) {
      const message = err.response?.data?.detail || "Invalid email or password";
      set({ error: message, isLoading: false, isAuthenticated: false });
      return false;
    }
  },

  logout: async () => {
    set({ isLoading: true });
    try {
      await api.post("/auth/logout");
    } catch {
      // Ignore errors on logout
    } finally {
      set({ user: null, isAuthenticated: false, isLoading: false, error: null });
    }
  },

  checkSession: async () => {
    set({ isLoading: true });
    try {
      const res = await api.get("/auth/me");
      if (res.status === 200 && res.data.id) {
        set({ user: res.data as User, isAuthenticated: true, isLoading: false });
        return true;
      }
      set({ user: null, isAuthenticated: false, isLoading: false });
      return false;
    } catch {
      // No valid session — not logged in
      set({ user: null, isAuthenticated: false, isLoading: false });
      return false;
    }
  },
}));
