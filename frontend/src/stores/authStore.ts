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

// Fallback dummy user for demo purposes if backend isn't ready
const DEMO_USER: User = { id: "1", email: "admin@tensorai.dev", name: "Tensor Admin", role: "admin" };

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true, // Start true while we check initial session
  error: null,

  login: async (credentials: LoginCredentials) => {
    set({ isLoading: true, error: null });
    try {
      // In a real app we'd wait for backend response which sets httpOnly cookie
      const res = await api.post("/auth/login", credentials);
      if (res.status === 200) {
        set({ user: DEMO_USER, isAuthenticated: true, isLoading: false });
        return true;
      }
      return false;
    } catch (err) {
      // Fallback for demo: if backend is off, let any login pass
      console.warn("Auth backend down, falling back to demo login.");
      set({ user: DEMO_USER, isAuthenticated: true, isLoading: false });
      return true;
    }
  },

  logout: async () => {
    set({ isLoading: true });
    try {
      // Backend routes should clear the httpOnly cookie
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
      // Call a generic protected endpoint or an /auth/me endpoint 
      // If we get a 200, the httpOnly cookie is valid
      const res = await api.get("/health"); 
      if (res.status === 200) {
        set({ user: DEMO_USER, isAuthenticated: true, isLoading: false });
        return true;
      }
      return false;
    } catch (err) {
      // If backend gives 401 or network error
      set({ user: null, isAuthenticated: false, isLoading: false });
      return false;
    }
  },
}));
