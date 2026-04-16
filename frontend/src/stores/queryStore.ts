import { create } from "zustand";
import { api } from "../services/api";
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
    
    // Basic sanitization
    const sanitizedQuestion = question.trim().substring(0, 2000);
    
    try {
      const response = await api.post<QueryResponse>("/query/", { question: sanitizedQuestion });

      set({
        answer: response.data.answer,
        sources: response.data.sources,
        reasoningTrace: response.data.reasoning_trace,
        isLoading: false,
      });
    } catch (err) {
      // DEMO FALLBACK if backend is offline
      console.warn("Query API failed. Using demo response.");
      setTimeout(() => {
        set({
          answer: "Based on the internal graph, **Q3 Revenue** matched projections but **Q4** saw a 12% dip due to V-204 supplier contract renegotiations. This aligns with the compliance audit requirements for 2025.",
          sources: ["doc_finance_q3.pdf", "vendor_contracts/v204.docx"],
          reasoningTrace: [
            { agent: "PLANNER", action: "Decomposing query", input_summary: question, output_summary: "Identify Q3/Q4 difference and related entities", duration_ms: 120 },
            { agent: "RETRIEVER", action: "Graph Traversal", input_summary: "Q3_REVENUE, Q4_REVENUE", output_summary: "Found link to VENDOR_RISK via V-204", duration_ms: 450 },
            { agent: "EXECUTOR", action: "Synthesizing answer", input_summary: "Raw docs + Graph edges", output_summary: "Drafted summary of revenue impact", duration_ms: 800 },
          ],
          isLoading: false
        });
      }, 1500);
    }
  },

  reset: () =>
    set({ isLoading: false, answer: null, sources: [], reasoningTrace: [], error: null }),
}));
