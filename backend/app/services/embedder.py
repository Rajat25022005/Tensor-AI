"""Embedding service — generates vector embeddings using sentence-transformers."""

import asyncio
from dataclasses import dataclass, field
from functools import partial

from app.core.config import settings
from app.core.logging import logger


@dataclass
class EmbeddingService:
    """Generates embeddings using a local sentence-transformers model.

    The model is lazy-loaded on first use and cached for subsequent calls.
    Encoding runs in a thread pool to avoid blocking the async event loop.
    """

    model_name: str = settings.EMBEDDING_MODEL
    dimension: int = settings.EMBEDDING_DIMENSION
    _model: object = field(default=None, repr=False)

    def _load_model(self) -> None:
        """Synchronously load the sentence-transformers model (called once)."""
        if self._model is not None:
            return

        logger.info("embedder.loading_model", model=self.model_name)
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            actual_dim = self._model.get_sentence_embedding_dimension()
            logger.info(
                "embedder.model_loaded",
                model=self.model_name,
                dimension=actual_dim,
            )
            if actual_dim != self.dimension:
                logger.warning(
                    "embedder.dimension_mismatch",
                    configured=self.dimension,
                    actual=actual_dim,
                    message="Update EMBEDDING_DIMENSION in config to match model.",
                )
                self.dimension = actual_dim
        except ImportError:
            logger.error(
                "embedder.import_error",
                message="sentence-transformers not installed. Using zero vectors.",
            )
        except Exception as exc:
            logger.error("embedder.load_failed", error=str(exc))

    def _encode_sync(self, texts: list[str]) -> list[list[float]]:
        """Synchronous encoding — called inside a thread pool."""
        self._load_model()
        if self._model is None:
            return [[0.0] * self.dimension for _ in texts]

        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            batch_size=32,
        )
        return [emb.tolist() for emb in embeddings]

    async def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""
        results = await self.embed_batch([text])
        return results[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts.

        Offloads the CPU-bound encoding to a thread pool so we don't
        block the async event loop.
        """
        if not texts:
            return []

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(self._encode_sync, texts))
