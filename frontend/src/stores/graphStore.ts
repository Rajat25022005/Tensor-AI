import { create } from "zustand";
import { api } from "../services/api";
import type { GraphNode, GraphEdge, GraphData } from "../types";

// Mock graph data for the explorer
const DEMO_GRAPH_DATA: GraphData = {
  nodes: [
    { id: "1", name: "CENTRAL_ID_CORP", type: "COMPANY" },
    { id: "2", name: "VENDOR_RISK", type: "RISK_REPORT" },
    { id: "3", name: "COMPLIANCE_2025", type: "COMPLIANCE" },
    { id: "4", name: "Q4_REVENUE", type: "FINANCE" },
    { id: "5", name: "LEGAL_CONTRACTS", type: "LEGAL" },
    { id: "6", name: "V-204_SUPPLIER", type: "VENDOR" },
    { id: "7", name: "AUDIT_Q3", type: "AUDIT" }
  ],
  edges: [
    { source: "1", target: "2", label: "HAS_RISK" },
    { source: "1", target: "3", label: "MUST_COMPLY" },
    { source: "1", target: "4", label: "REPORTED_REV" },
    { source: "1", target: "5", label: "OWNS_CONTRACT" },
    { source: "2", target: "6", label: "AFFECTS" },
    { source: "3", target: "7", label: "VALIDATED_BY" },
  ]
};

interface GraphState {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNodeId: string | null;
  isLoading: boolean;
  error: string | null;
  setSelectedNode: (id: string | null) => void;
  fetchSubgraph: (entityId?: string) => Promise<void>;
}

export const useGraphStore = create<GraphState>((set) => ({
  nodes: DEMO_GRAPH_DATA.nodes,
  edges: DEMO_GRAPH_DATA.edges,
  selectedNodeId: null,
  isLoading: false,
  error: null,

  setSelectedNode: (id) => set({ selectedNodeId: id }),

  fetchSubgraph: async (entityId: string = "root") => {
    set({ isLoading: true, error: null });
    try {
      // const response = await api.get(`/graph/${entityId}`);
      // set({ nodes: response.data.nodes, edges: response.data.edges, isLoading: false });
      
      // Stand-in for demo
      await new Promise(resolve => setTimeout(resolve, 600));
      set({ 
        nodes: DEMO_GRAPH_DATA.nodes, 
        edges: DEMO_GRAPH_DATA.edges, 
        isLoading: false 
      });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },
}));
