import { create } from "zustand";
import { api } from "../services/api";
import type { ConnectorConfig } from "../types";

// Mock initial data if backend is offline
const DEMO_CONNECTORS: ConnectorConfig[] = [
  {
    id: "pdf-1",
    type: "pdf",
    name: "Local PDF Ingestion",
    status: "connected",
    config: { directory: "/data/docs" },
    lastSync: new Date().toISOString(),
  },
  {
    id: "gmail-1",
    type: "gmail",
    name: "Support Inbox",
    status: "disconnected",
    config: { email: "support@tensorai.demo" },
  },
  {
    id: "slack-1",
    type: "slack",
    name: "Engineering Slack",
    status: "disconnected",
    config: { workspace: "tensor-eng" },
  },
];

interface LLMConfig {
  model: string;
  temperature: number;
  maxTokens: number;
}

interface SettingsState {
  connectors: ConnectorConfig[];
  llmConfig: LLMConfig;
  isLoading: boolean;
  error: string | null;
  fetchConnectors: () => Promise<void>;
  toggleConnectorStatus: (id: string) => Promise<void>;
  updateLLMConfig: (config: LLMConfig) => Promise<void>;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  connectors: DEMO_CONNECTORS,
  llmConfig: {
    model: "mistral",
    temperature: 0.1,
    maxTokens: 2048,
  },
  isLoading: false,
  error: null,

  fetchConnectors: async () => {
    set({ isLoading: true, error: null });
    try {
      // In a real implementation this would fetch from backend
      // const response = await api.get("/connectors");
      // set({ connectors: response.data, isLoading: false });
      
      // Simulate network request
      await new Promise(resolve => setTimeout(resolve, 500));
      set({ isLoading: false });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  toggleConnectorStatus: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      // Simulate backend toggle
      await new Promise(resolve => setTimeout(resolve, 600));
      const newConnectors = get().connectors.map(c => {
        if (c.id === id) {
          return { ...c, status: c.status === "connected" ? "disconnected" as const : "connected" as const, lastSync: new Date().toISOString() };
        }
        return c;
      });
      set({ connectors: newConnectors, isLoading: false });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  updateLLMConfig: async (config: LLMConfig) => {
    set({ isLoading: true, error: null });
    try {
      // Simulate backend update
      await new Promise(resolve => setTimeout(resolve, 400));
      set({ llmConfig: config, isLoading: false });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  }
}));
