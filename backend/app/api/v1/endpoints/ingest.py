"""Ingestion endpoint — upload documents for processing."""

from fastapi import APIRouter, UploadFile, File

from app.models.schemas.ingest import IngestResponse

router = APIRouter()


@router.post("/upload", response_model=IngestResponse, summary="Upload a document")
async def upload_document(file: UploadFile = File(...)) -> IngestResponse:
    """Accept a file upload and queue it for ingestion."""
    # TODO: wire up IngestionPipeline
    return IngestResponse(
        filename=file.filename or "unknown",
        status="queued",
        message="Document received and queued for processing.",
    )
