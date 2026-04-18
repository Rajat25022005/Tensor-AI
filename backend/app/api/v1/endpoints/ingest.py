"""Ingestion endpoint — upload documents for processing."""

import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from app.models.schemas.ingest import IngestResponse
from app.services.ingestion import IngestionPipeline
from app.connectors.pdf_connector import PDFConnector
from app.core.dependencies import get_ingestion_pipeline
from app.core.logging import logger

router = APIRouter()


@router.post("/upload", response_model=IngestResponse, summary="Upload a document")
async def upload_document(
    file: UploadFile = File(...),
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestResponse:
    """Accept a file upload and process it through the ingestion pipeline."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    # Validate file type
    allowed_extensions = {".pdf", ".txt", ".md", ".csv", ".json"}
    extension = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {extension}. Allowed: {', '.join(allowed_extensions)}",
        )

    document_id = str(uuid.uuid4())[:12]

    try:
        # Read file content
        raw_bytes = await file.read()
        content = ""

        if extension == ".pdf":
            # Extract text from PDF using pypdf
            content = await _extract_pdf_text(raw_bytes)
        else:
            # Plain text files
            content = raw_bytes.decode("utf-8", errors="replace")

        if not content.strip():
            return IngestResponse(
                filename=file.filename,
                status="failed",
                message="Could not extract any text content from the file.",
                document_id=document_id,
            )

        # Run the ingestion pipeline
        result = await pipeline.ingest(content=content, filename=file.filename)

        logger.info(
            "ingest.upload.success",
            filename=file.filename,
            document_id=document_id,
            chunks=result.get("chunks_created", 0),
            entities=result.get("entities_extracted", 0),
        )

        return IngestResponse(
            filename=file.filename,
            status="completed",
            message="Document processed successfully.",
            document_id=document_id,
            chunks_created=result.get("chunks_created"),
            entities_extracted=result.get("entities_extracted"),
        )

    except Exception as exc:
        logger.error("ingest.upload.failed", filename=file.filename, error=str(exc))
        return IngestResponse(
            filename=file.filename,
            status="failed",
            message=f"Ingestion failed: {str(exc)}",
            document_id=document_id,
        )


async def _extract_pdf_text(raw_bytes: bytes) -> str:
    """Extract text from PDF bytes using pypdf."""
    import io
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(raw_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n\n".join(pages)
    except Exception as exc:
        logger.warning("ingest.pdf_extract_failed", error=str(exc))
        return ""
