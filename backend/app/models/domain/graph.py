"""Domain models for graph entities and relationships."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entity:
    """A node in the knowledge graph."""

    id: str
    name: str
    entity_type: str
    properties: dict[str, str | int | float | bool] = field(default_factory=dict)
    source_document: str | None = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Relationship:
    """An edge connecting two entities in the knowledge graph."""

    source_id: str
    target_id: str
    relation_type: str
    properties: dict[str, str | int | float | bool] = field(default_factory=dict)
    confidence: float = 1.0
    temporal: bool = False
    timestamp: datetime | None = None


@dataclass
class Document:
    """A source document that has been ingested."""

    id: str
    filename: str
    content_hash: str
    chunk_count: int = 0
    entity_count: int = 0
    status: str = "pending"
    ingested_at: datetime = field(default_factory=datetime.now)
