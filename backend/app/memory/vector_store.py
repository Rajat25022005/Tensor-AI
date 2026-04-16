"""Vector store abstraction — supports ChromaDB and Qdrant backends."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class VectorStoreBase(ABC):
    """Abstract base for vector store implementations."""

    @abstractmethod
    async def add_documents(self, documents: list[dict]) -> None:
        """Add document chunks with embeddings to the store."""
        ...

    @abstractmethod
    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search for similar documents by embedding."""
        ...

    @abstractmethod
    async def delete(self, document_ids: list[str]) -> None:
        """Delete documents by their IDs."""
        ...


class ChromaDBStore(VectorStoreBase):
    """ChromaDB vector store implementation."""

    def __init__(self) -> None:
        # TODO: initialize ChromaDB client
        pass

    async def add_documents(self, documents: list[dict]) -> None:
        """Add documents to ChromaDB."""
        # TODO: implement
        pass

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search ChromaDB by embedding similarity."""
        # TODO: implement
        return []

    async def delete(self, document_ids: list[str]) -> None:
        """Delete from ChromaDB."""
        # TODO: implement
        pass


class QdrantStore(VectorStoreBase):
    """Qdrant vector store implementation."""

    def __init__(self) -> None:
        # TODO: initialize Qdrant client
        pass

    async def add_documents(self, documents: list[dict]) -> None:
        """Add documents to Qdrant."""
        # TODO: implement
        pass

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search Qdrant by embedding similarity."""
        # TODO: implement
        return []

    async def delete(self, document_ids: list[str]) -> None:
        """Delete from Qdrant."""
        # TODO: implement
        pass


def get_vector_store(provider: str = "chromadb") -> VectorStoreBase:
    """Factory to return the configured vector store."""
    stores = {
        "chromadb": ChromaDBStore,
        "qdrant": QdrantStore,
    }
    store_cls = stores.get(provider)
    if store_cls is None:
        raise ValueError(f"Unknown vector store provider: {provider}")
    return store_cls()
