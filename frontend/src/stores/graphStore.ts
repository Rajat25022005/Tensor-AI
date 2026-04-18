import { create } from "zustand";
import { api } from "../services/api";
import type { GraphNode, GraphEdge } from "../types";

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
  nodes: [],
  edges: [],
  selectedNodeId: null,
  isLoading: false,
  error: null,

  setSelectedNode: (id) => set({ selectedNodeId: id }),

  fetchSubgraph: async (entityId?: string) => {
    set({ isLoading: true, error: null });
    try {
      const endpoint = entityId ? `/graph/${entityId}` : "/graph/";
      const response = await api.get(endpoint);
      
      const data = response.data;
      
      // The graph stats endpoint returns { graph_nodes, vector_documents }
      // The subgraph endpoint returns { nodes, edges }
      if (data.nodes) {
        set({ 
          nodes: data.nodes as GraphNode[], 
          edges: data.edges as GraphEdge[], 
          isLoading: false 
        });
      } else {
        // Stats endpoint — no subgraph to display yet
        set({ nodes: [], edges: [], isLoading: false });
      }
    } catch (err) {
      console.warn("Graph API failed.", err);
      set({ 
        nodes: [], 
        edges: [], 
        error: "Could not load graph data", 
        isLoading: false 
      });
    }
  },
}));
