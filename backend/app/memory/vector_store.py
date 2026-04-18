"""Vector store abstraction — supports ChromaDB and Qdrant backends."""

import uuid
from abc import ABC, abstractmethod

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import VectorStoreError


COLLECTION_NAME = "tensorai_documents"


class VectorStoreBase(ABC):
    """Abstract base for vector store implementations."""

    @abstractmethod
    async def add_documents(self, documents: list[dict]) -> None:
        """Add document chunks with embeddings to the store.

        Each document dict must contain: id, text, embedding.
        May also contain arbitrary metadata keys.
        """
        ...

    @abstractmethod
    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search for similar documents by embedding.

        Returns a list of dicts with: id, text, score, and metadata.
        """
        ...

    @abstractmethod
    async def delete(self, document_ids: list[str]) -> None:
        """Delete documents by their IDs."""
        ...

    @abstractmethod
    async def count(self) -> int:
        """Return the number of documents in the store."""
        ...


class ChromaDBStore(VectorStoreBase):
    """ChromaDB vector store implementation."""

    def __init__(self) -> None:
        try:
            import chromadb

            self._client = chromadb.HttpClient(
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT,
            )
            self._collection = self._client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(
                "vector_store.chromadb.connected",
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT,
            )
        except Exception as exc:
            logger.error("vector_store.chromadb.init_failed", error=str(exc))
            raise VectorStoreError(f"Failed to connect to ChromaDB: {exc}") from exc

    async def add_documents(self, documents: list[dict]) -> None:
        """Add documents to ChromaDB."""
        if not documents:
            return

        ids = [doc.get("id", str(uuid.uuid4())) for doc in documents]
        embeddings = [doc["embedding"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadatas = []
        for doc in documents:
            meta = {k: v for k, v in doc.items() if k not in ("id", "text", "embedding")}
            # ChromaDB metadata values must be str, int, float, or bool
            clean_meta = {}
            for k, v in meta.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_meta[k] = v
                else:
                    clean_meta[k] = str(v)
            metadatas.append(clean_meta)

        try:
            self._collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
            )
            logger.info("vector_store.chromadb.added", count=len(documents))
        except Exception as exc:
            logger.error("vector_store.chromadb.add_failed", error=str(exc))
            raise VectorStoreError(f"ChromaDB add failed: {exc}") from exc

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search ChromaDB by embedding similarity."""
        try:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )

            documents = []
            if results["ids"] and results["ids"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    # ChromaDB returns distances; cosine distance → similarity = 1 - distance
                    distance = results["distances"][0][i] if results["distances"] else 0.0
                    score = 1.0 - distance

                    documents.append({
                        "id": doc_id,
                        "text": results["documents"][0][i] if results["documents"] else "",
                        "score": round(score, 4),
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    })

            return documents
        except Exception as exc:
            logger.error("vector_store.chromadb.search_failed", error=str(exc))
            raise VectorStoreError(f"ChromaDB search failed: {exc}") from exc

    async def delete(self, document_ids: list[str]) -> None:
        """Delete from ChromaDB."""
        if not document_ids:
            return
        try:
            self._collection.delete(ids=document_ids)
            logger.info("vector_store.chromadb.deleted", count=len(document_ids))
        except Exception as exc:
            logger.error("vector_store.chromadb.delete_failed", error=str(exc))
            raise VectorStoreError(f"ChromaDB delete failed: {exc}") from exc

    async def count(self) -> int:
        """Return document count in ChromaDB."""
        try:
            return self._collection.count()
        except Exception:
            return 0


class QdrantStore(VectorStoreBase):
    """Qdrant vector store implementation."""

    def __init__(self) -> None:
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            self._client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
            )

            # Create collection if it doesn't exist
            collections = [c.name for c in self._client.get_collections().collections]
            if COLLECTION_NAME not in collections:
                self._client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=settings.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE,
                    ),
                )

            logger.info(
                "vector_store.qdrant.connected",
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
            )
        except Exception as exc:
            logger.error("vector_store.qdrant.init_failed", error=str(exc))
            raise VectorStoreError(f"Failed to connect to Qdrant: {exc}") from exc

    async def add_documents(self, documents: list[dict]) -> None:
        """Add documents to Qdrant."""
        if not documents:
            return

        try:
            from qdrant_client.models import PointStruct

            points = []
            for doc in documents:
                doc_id = doc.get("id", str(uuid.uuid4()))
                payload = {k: v for k, v in doc.items() if k not in ("embedding",)}
                points.append(
                    PointStruct(
                        id=doc_id if doc_id.isdigit() else str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id)),
                        vector=doc["embedding"],
                        payload=payload,
                    )
                )

            self._client.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
            )
            logger.info("vector_store.qdrant.added", count=len(documents))
        except Exception as exc:
            logger.error("vector_store.qdrant.add_failed", error=str(exc))
            raise VectorStoreError(f"Qdrant add failed: {exc}") from exc

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search Qdrant by embedding similarity."""
        try:
            results = self._client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_embedding,
                limit=top_k,
                with_payload=True,
            ).points

            documents = []
            for point in results:
                documents.append({
                    "id": str(point.id),
                    "text": point.payload.get("text", "") if point.payload else "",
                    "score": round(point.score, 4),
                    "metadata": {
                        k: v for k, v in (point.payload or {}).items()
                        if k not in ("text", "embedding")
                    },
                })

            return documents
        except Exception as exc:
            logger.error("vector_store.qdrant.search_failed", error=str(exc))
            raise VectorStoreError(f"Qdrant search failed: {exc}") from exc

    async def delete(self, document_ids: list[str]) -> None:
        """Delete from Qdrant."""
        if not document_ids:
            return
        try:
            from qdrant_client.models import PointIdsList

            point_ids = []
            for did in document_ids:
                point_ids.append(did if did.isdigit() else str(uuid.uuid5(uuid.NAMESPACE_DNS, did)))

            self._client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=PointIdsList(points=point_ids),
            )
            logger.info("vector_store.qdrant.deleted", count=len(document_ids))
        except Exception as exc:
            logger.error("vector_store.qdrant.delete_failed", error=str(exc))
            raise VectorStoreError(f"Qdrant delete failed: {exc}") from exc

    async def count(self) -> int:
        """Return document count in Qdrant."""
        try:
            info = self._client.get_collection(COLLECTION_NAME)
            return info.points_count or 0
        except Exception:
            return 0


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
