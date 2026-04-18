import { create } from "zustand";
import { api } from "../services/api";
import type { DashboardStats, ReasoningStep } from "../types";

interface DashboardState {
  stats: DashboardStats | null;
  recentLogs: ReasoningStep[];
  isLoading: boolean;
  error: string | null;
  fetchDashboardData: () => Promise<void>;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  stats: null,
  recentLogs: [],
  isLoading: false,
  error: null,

  fetchDashboardData: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await api.get("/dashboard/stats");
      
      set({ 
        stats: res.data as DashboardStats,
        isLoading: false 
      });
    } catch (err) {
      console.warn("Dashboard API failed, using fallback.", err);
      // Graceful fallback if backend is offline
      set({ 
        stats: {
          graphNodes: 0,
          graphNodesTrend: 0,
          agentConfidence: 0,
          validatedTraces: 0,
          pendingTasks: 0,
        },
        isLoading: false,
        error: "Backend unreachable — showing empty state"
      });
    }
  },
}));
