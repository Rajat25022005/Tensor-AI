import { create } from "zustand";
import { api } from "../services/api";
import type { QueryResponse, ReasoningStep } from "../types";

interface QueryState {
  isLoading: boolean;
  answer: string | null;
  sources: string[];
  reasoningTrace: ReasoningStep[];
  confidence: number;
  error: string | null;
  submitQuery: (question: string) => Promise<void>;
  reset: () => void;
}

export const useQueryStore = create<QueryState>((set) => ({
  isLoading: false,
  answer: null,
  sources: [],
  reasoningTrace: [],
  confidence: 0,
  error: null,

  submitQuery: async (question: string) => {
    set({ isLoading: true, error: null, answer: null, confidence: 0 });
    
    const sanitizedQuestion = question.trim().substring(0, 2000);
    
    try {
      const response = await api.post<QueryResponse>("/query/", { 
        question: sanitizedQuestion 
      });

      set({
        answer: response.data.answer,
        sources: response.data.sources,
        reasoningTrace: response.data.reasoning_trace,
        confidence: response.data.confidence,
        isLoading: false,
      });
    } catch (err: any) {
      const message = err.response?.data?.detail || "Query failed. Is the backend running?";
      set({
        error: message,
        isLoading: false,
      });
    }
  },

  reset: () =>
    set({ isLoading: false, answer: null, sources: [], reasoningTrace: [], confidence: 0, error: null }),
}));
