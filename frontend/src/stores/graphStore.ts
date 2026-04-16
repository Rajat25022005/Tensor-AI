import { create } from "zustand";

interface GraphNode {
  id: string;
  name: string;
  type: string;
}

interface GraphEdge {
  source: string;
  target: string;
  label: string;
}

interface GraphState {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNodeId: string | null;
  isLoading: boolean;
  setSelectedNode: (id: string | null) => void;
  fetchSubgraph: (entityId: string) => Promise<void>;
}

export const useGraphStore = create<GraphState>((set) => ({
  nodes: [],
  edges: [],
  selectedNodeId: null,
  isLoading: false,

  setSelectedNode: (id) => set({ selectedNodeId: id }),

  fetchSubgraph: async (entityId: string) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`/api/v1/graph/${entityId}`);
      if (!response.ok) throw new Error("Failed to fetch subgraph");
      const data = await response.json();
      set({ nodes: data.nodes, edges: data.edges, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },
}));
