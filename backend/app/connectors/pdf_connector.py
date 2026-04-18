"""PDF connector — extracts text from PDF documents."""

import io
from collections.abc import AsyncGenerator
from pathlib import Path

from app.connectors.base import BaseConnector, ConnectorMetadata
from app.core.logging import logger


class PDFConnector(BaseConnector):
    """Extracts text content from uploaded PDF files.

    Supports both file-path-based and raw-bytes-based extraction.
    """

    def __init__(self, watch_directory: str | None = None) -> None:
        self._watch_directory = watch_directory
        self._connected = False
        self._document_count = 0

    async def connect(self) -> None:
        """Mark the PDF connector as ready."""
        self._connected = True
        logger.info("pdf_connector.connected")

    async def disconnect(self) -> None:
        """Disconnect the PDF connector."""
        self._connected = False
        logger.info("pdf_connector.disconnected")

    async def fetch_documents(self) -> AsyncGenerator[dict, None]:
        """Scan the watch directory and yield PDFs as documents.

        Each yielded dict contains: content (extracted text), metadata (filename, pages, etc.)
        """
        if not self._watch_directory:
            logger.info("pdf_connector.no_watch_dir", message="No watch directory configured")
            return

        watch_path = Path(self._watch_directory)
        if not watch_path.exists():
            logger.warning("pdf_connector.dir_not_found", path=self._watch_directory)
            return

        for pdf_file in watch_path.glob("**/*.pdf"):
            try:
                content, page_count = self._extract_from_path(pdf_file)
                if content.strip():
                    self._document_count += 1
                    yield {
                        "content": content,
                        "metadata": {
                            "filename": pdf_file.name,
                            "filepath": str(pdf_file),
                            "pages": page_count,
                            "source": "pdf_connector",
                        },
                    }
                    logger.info(
                        "pdf_connector.extracted",
                        filename=pdf_file.name,
                        pages=page_count,
                        chars=len(content),
                    )
            except Exception as exc:
                logger.error(
                    "pdf_connector.extraction_failed",
                    filename=pdf_file.name,
                    error=str(exc),
                )

    async def get_metadata(self) -> ConnectorMetadata:
        """Return PDF connector metadata."""
        return ConnectorMetadata(
            name="PDF Connector",
            connector_type="pdf",
            is_connected=self._connected,
            document_count=self._document_count,
        )

    # ── Extraction methods ───────────────────────────────────────────────

    @staticmethod
    def _extract_from_path(filepath: Path) -> tuple[str, int]:
        """Extract text from a PDF file on disk.

        Returns:
            A tuple of (full_text, page_count).
        """
        from pypdf import PdfReader

        reader = PdfReader(str(filepath))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())

        return "\n\n".join(pages), len(reader.pages)

    @staticmethod
    def extract_from_bytes(raw_bytes: bytes) -> tuple[str, int]:
        """Extract text from raw PDF bytes (e.g., from an upload).

        Returns:
            A tuple of (full_text, page_count).
        """
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(raw_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())

        return "\n\n".join(pages), len(reader.pages)
