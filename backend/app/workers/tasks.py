"""Background tasks for document ingestion."""

import asyncio

from app.workers.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def ingest_document_task(self, document_id: str, content: str, filename: str) -> dict:
    """Background task: process a document through the ingestion pipeline.

    This runs outside the request cycle for large documents.
    Uses asyncio bridge since Celery workers are synchronous.
    """
    logger.info("task.ingest_document.start", document_id=document_id, filename=filename)

    try:
        result = asyncio.get_event_loop().run_until_complete(
            _run_ingestion(content, filename)
        )
        logger.info(
            "task.ingest_document.complete",
            document_id=document_id,
            chunks=result.get("chunks_created", 0),
        )
        return {"status": "completed", "document_id": document_id, **result}
    except RuntimeError:
        # No running event loop — create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_run_ingestion(content, filename))
            logger.info(
                "task.ingest_document.complete",
                document_id=document_id,
                chunks=result.get("chunks_created", 0),
            )
            return {"status": "completed", "document_id": document_id, **result}
        finally:
            loop.close()
    except Exception as exc:
        logger.error(
            "task.ingest_document.failed",
            document_id=document_id,
            error=str(exc),
        )
        raise self.retry(exc=exc)


async def _run_ingestion(content: str, filename: str) -> dict:
    """Async bridge: instantiate pipeline components and run ingestion."""
    from app.services.chunker import TextChunker
    from app.services.embedder import EmbeddingService
    from app.memory.entity_extractor import EntityExtractor
    from app.memory.graph_memory import GraphMemory
    from app.memory.vector_store import get_vector_store
    from app.services.llm import LLMService
    from app.services.ingestion import IngestionPipeline
    from app.core.config import settings

    llm = LLMService()
    graph_memory = GraphMemory()
    vector_store = get_vector_store(settings.VECTOR_STORE_PROVIDER)

    pipeline = IngestionPipeline(
        chunker=TextChunker(),
        embedder=EmbeddingService(),
        extractor=EntityExtractor(llm=llm),
        graph_memory=graph_memory,
        vector_store=vector_store,
    )

    try:
        return await pipeline.ingest(content=content, filename=filename)
    finally:
        await graph_memory.close()
