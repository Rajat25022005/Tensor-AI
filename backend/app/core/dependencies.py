"""Dependency injection providers for FastAPI."""

from functools import lru_cache

from app.core.config import Settings, settings
from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase, get_vector_store
from app.memory.hybrid_retriever import HybridRetriever
from app.memory.entity_extractor import EntityExtractor
from app.services.llm import LLMService
from app.services.embedder import EmbeddingService
from app.services.chunker import TextChunker
from app.services.ingestion import IngestionPipeline
from app.connectors.registry import ConnectorRegistry
from app.agents.orchestrator import AgentOrchestrator


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


# ── Singleton instances ──────────────────────────────────────────────────────
# Initialized during startup via lifecycle.py, accessed via these getters.

_graph_memory: GraphMemory | None = None
_vector_store: VectorStoreBase | None = None
_llm_service: LLMService | None = None
_embedding_service: EmbeddingService | None = None
_connector_registry: ConnectorRegistry | None = None
_ingestion_pipeline: IngestionPipeline | None = None
_orchestrator: AgentOrchestrator | None = None


def init_services() -> None:
    """Initialize all service singletons. Called once during app startup."""
    global _graph_memory, _vector_store, _llm_service, _embedding_service
    global _connector_registry, _ingestion_pipeline, _orchestrator

    _graph_memory = GraphMemory()
    _vector_store = get_vector_store(settings.VECTOR_STORE_PROVIDER)
    _llm_service = LLMService()
    _embedding_service = EmbeddingService()
    _connector_registry = ConnectorRegistry()

    _ingestion_pipeline = IngestionPipeline(
        chunker=TextChunker(),
        embedder=_embedding_service,
        extractor=EntityExtractor(llm=_llm_service),
        graph_memory=_graph_memory,
        vector_store=_vector_store,
    )

    _orchestrator = AgentOrchestrator(
        llm=_llm_service,
        graph_memory=_graph_memory,
        vector_store=_vector_store,
        embedder=_embedding_service,
    )


async def close_services() -> None:
    """Gracefully close all service connections. Called during app shutdown."""
    if _graph_memory:
        await _graph_memory.close()


# ── FastAPI dependency getters ───────────────────────────────────────────────

def get_graph_memory() -> GraphMemory:
    """FastAPI dependency: return the GraphMemory singleton."""
    assert _graph_memory is not None, "GraphMemory not initialized. Check startup."
    return _graph_memory


def get_vector_store_dep() -> VectorStoreBase:
    """FastAPI dependency: return the VectorStore singleton."""
    assert _vector_store is not None, "VectorStore not initialized. Check startup."
    return _vector_store


def get_llm_service() -> LLMService:
    """FastAPI dependency: return the LLMService singleton."""
    assert _llm_service is not None, "LLMService not initialized. Check startup."
    return _llm_service


def get_embedding_service() -> EmbeddingService:
    """FastAPI dependency: return the EmbeddingService singleton."""
    assert _embedding_service is not None, "EmbeddingService not initialized. Check startup."
    return _embedding_service


def get_connector_registry() -> ConnectorRegistry:
    """FastAPI dependency: return the ConnectorRegistry singleton."""
    assert _connector_registry is not None, "ConnectorRegistry not initialized. Check startup."
    return _connector_registry


def get_ingestion_pipeline() -> IngestionPipeline:
    """FastAPI dependency: return the IngestionPipeline singleton."""
    assert _ingestion_pipeline is not None, "IngestionPipeline not initialized. Check startup."
    return _ingestion_pipeline


def get_orchestrator() -> AgentOrchestrator:
    """FastAPI dependency: return the AgentOrchestrator singleton."""
    assert _orchestrator is not None, "AgentOrchestrator not initialized. Check startup."
    return _orchestrator
