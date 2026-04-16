import { create } from "zustand";
import type { QueryResponse, ReasoningStep } from "../types";

interface QueryState {
  isLoading: boolean;
  answer: string | null;
  sources: string[];
  reasoningTrace: ReasoningStep[];
  error: string | null;
  submitQuery: (question: string) => Promise<void>;
  reset: () => void;
}

export const useQueryStore = create<QueryState>((set) => ({
  isLoading: false,
  answer: null,
  sources: [],
  reasoningTrace: [],
  error: null,

  submitQuery: async (question: string) => {
    set({ isLoading: true, error: null, answer: null });
    try {
      const response = await fetch("/api/v1/query/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) throw new Error(`Request failed: ${response.status}`);

      const data: QueryResponse = await response.json();
      set({
        answer: data.answer,
        sources: data.sources,
        reasoningTrace: data.reasoning_trace,
        isLoading: false,
      });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  reset: () =>
    set({ isLoading: false, answer: null, sources: [], reasoningTrace: [], error: null }),
}));
