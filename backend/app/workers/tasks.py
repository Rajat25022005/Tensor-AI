"""Background tasks for document ingestion."""

from app.workers.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def ingest_document_task(self, document_id: str, content: str, filename: str) -> dict:
    """Background task: process a document through the ingestion pipeline.

    This runs outside the request cycle for large documents.
    """
    logger.info("task.ingest_document.start", document_id=document_id, filename=filename)
    try:
        # TODO: call IngestionPipeline synchronously (or use async bridge)
        return {"status": "completed", "document_id": document_id}
    except Exception as exc:
        logger.error("task.ingest_document.failed", document_id=document_id, error=str(exc))
        raise self.retry(exc=exc)
