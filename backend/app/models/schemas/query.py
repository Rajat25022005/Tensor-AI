"""Query request/response schemas."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Incoming user query."""

    question: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    session_id: str | None = Field(default=None, description="Optional session ID for context")
    max_depth: int = Field(default=3, ge=1, le=10, description="Max graph traversal depth")


class ReasoningStep(BaseModel):
    """A single step in the agent's reasoning trace."""

    agent: str
    action: str
    input_summary: str
    output_summary: str
    duration_ms: float


class QueryResponse(BaseModel):
    """Response from the multi-agent pipeline."""

    answer: str
    sources: list[str] = Field(default_factory=list)
    reasoning_trace: list[ReasoningStep] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
