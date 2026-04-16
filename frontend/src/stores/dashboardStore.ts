import { create } from "zustand";
import { api } from "../services/api";
import type { DashboardStats, ReasoningStep } from "../types";

// Mock initial data so the dashboard is functional stand-alone
const DEMO_STATS: DashboardStats = {
  graphNodes: 128492,
  graphNodesTrend: 14200,
  agentConfidence: 98.4,
  validatedTraces: 2400,
  pendingTasks: 4,
};

const DEMO_LOGS: ReasoningStep[] = [
  { agent: "PLAN", action: "Analyzing vendor variance...", input_summary: "", output_summary: "Analyzing vendor variance...", duration_ms: 124 },
  { agent: "RETR", action: "Fetching nodes: 'V-204', 'V-205'", input_summary: "", output_summary: "Fetching nodes: 'V-204', 'V-205'", duration_ms: 432 },
  { agent: "EXEC", action: "Synthesizing cross-relational data", input_summary: "", output_summary: "Synthesizing cross-relational data", duration_ms: 1042 },
  { agent: "DONE", action: "Validation cycle completed", input_summary: "", output_summary: "Validation cycle completed", duration_ms: 85 },
];

interface DashboardState {
  stats: DashboardStats | null;
  recentLogs: ReasoningStep[];
  isLoading: boolean;
  error: string | null;
  fetchDashboardData: () => Promise<void>;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  stats: DEMO_STATS, // Start with demo data rendered
  recentLogs: DEMO_LOGS,
  isLoading: false,
  error: null,

  fetchDashboardData: async () => {
    set({ isLoading: true, error: null });
    try {
      // Check health endpoint for backend readiness
      await api.get("/health/ready");
      // TODO: Once backend provides stats endpoint, fetch it here
      // For now, we simulate a small delay to mimic fetching
      await new Promise(resolve => setTimeout(resolve, 800));
      
      set({ 
        stats: DEMO_STATS, 
        recentLogs: DEMO_LOGS,
        isLoading: false 
      });
    } catch (err) {
      // If backend is unreachable, we still keep the demo data but show an error silently in console
      console.warn("Backend unreachable, using demo dashboard data.");
      set({ 
        // fallback to demo data if API fails to keep UI functional
        stats: DEMO_STATS,
        recentLogs: DEMO_LOGS,
        isLoading: false,
        error: "Running in local demo mode (backend offline)"
      });
    }
  },
}));
