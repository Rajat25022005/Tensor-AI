import { create } from "zustand";
import { api } from "../services/api";
import type { ConnectorConfig } from "../types";

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
  connectors: [],
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
      const response = await api.get("/connectors/");
      const backendConnectors = response.data.connectors || [];
      
      // Map backend connector metadata to frontend ConnectorConfig shape
      const mapped: ConnectorConfig[] = backendConnectors.map((c: any, i: number) => ({
        id: `${c.connector_type}-${i + 1}`,
        type: c.connector_type,
        name: c.name,
        status: c.is_connected ? "connected" as const : "disconnected" as const,
        config: {},
        lastSync: c.is_connected ? new Date().toISOString() : undefined,
      }));
      
      set({ connectors: mapped, isLoading: false });
    } catch (err) {
      console.warn("Connectors API failed.", err);
      set({ 
        connectors: [],
        error: "Could not load connectors",
        isLoading: false 
      });
    }
  },

  toggleConnectorStatus: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      // Extract connector type name from the id (e.g., "pdf-1" → "pdf")
      const connectorName = id.split("-")[0];
      
      await api.post("/connectors/toggle", { connector_name: connectorName });
      
      // Refetch to get updated state from backend
      const response = await api.get("/connectors/");
      const backendConnectors = response.data.connectors || [];
      
      const mapped: ConnectorConfig[] = backendConnectors.map((c: any, i: number) => ({
        id: `${c.connector_type}-${i + 1}`,
        type: c.connector_type,
        name: c.name,
        status: c.is_connected ? "connected" as const : "disconnected" as const,
        config: {},
        lastSync: c.is_connected ? new Date().toISOString() : undefined,
      }));
      
      set({ connectors: mapped, isLoading: false });
    } catch (err: any) {
      const message = err.response?.data?.detail || "Toggle failed";
      set({ error: message, isLoading: false });
    }
  },

  updateLLMConfig: async (config: LLMConfig) => {
    set({ isLoading: true, error: null });
    try {
      // LLM config is currently stored client-side
      // TODO: POST /settings/llm once backend supports it
      set({ llmConfig: config, isLoading: false });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  }
}));
