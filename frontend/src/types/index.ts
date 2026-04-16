/* ── API Response Types ─────────────────────────────────────────────── */

export interface ReasoningStep {
  agent: string;
  action: string;
  input_summary: string;
  output_summary: string;
  duration_ms: number;
}

export interface QueryResponse {
  answer: string;
  sources: string[];
  reasoning_trace: ReasoningStep[];
  confidence: number;
}

export interface IngestResponse {
  filename: string;
  status: "queued" | "processing" | "completed" | "failed";
  message: string;
  document_id?: string;
  chunks_created?: number;
  entities_extracted?: number;
}

/* ── Graph Types ───────────────────────────────────────────────────── */

export interface GraphNode {
  id: string;
  name: string;
  type: string;
  properties?: Record<string, string | number | boolean>;
}

export interface GraphEdge {
  source: string;
  target: string;
  label: string;
  confidence?: number;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

/* ── Auth Types ────────────────────────────────────────────────────── */

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  expires_in: number;
}

/* ── Connector Types ───────────────────────────────────────────────── */

export interface ConnectorStatus {
  name: string;
  connector_type: string;
  is_connected: boolean;
  document_count: number;
}
