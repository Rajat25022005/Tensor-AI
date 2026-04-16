"""Ingestion request/response schemas."""

from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    """Response after a document is submitted for ingestion."""

    filename: str
    status: str = Field(default="queued", description="queued | processing | completed | failed")
    message: str
    document_id: str | None = None
    chunks_created: int | None = None
    entities_extracted: int | None = None
