"""Embedding service — generates vector embeddings for text."""

from dataclasses import dataclass

from app.core.config import settings
from app.core.logging import logger


@dataclass
class EmbeddingService:
    """Generates embeddings using a local sentence-transformers model."""

    model_name: str = settings.EMBEDDING_MODEL
    _model: object = None

    async def _load_model(self) -> None:
        """Lazy-load the embedding model."""
        if self._model is None:
            logger.info("embedder.loading_model", model=self.model_name)
            # TODO: load sentence-transformers model
            pass

    async def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""
        await self._load_model()
        # TODO: generate embedding
        return [0.0] * settings.EMBEDDING_DIMENSION

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        await self._load_model()
        # TODO: batch embedding generation
        return [[0.0] * settings.EMBEDDING_DIMENSION for _ in texts]
