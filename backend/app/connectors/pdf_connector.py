"""PDF connector — extracts text from PDF documents."""

from collections.abc import AsyncGenerator

from app.connectors.base import BaseConnector, ConnectorMetadata
from app.core.logging import logger


class PDFConnector(BaseConnector):
    """Extracts text content from uploaded PDF files."""

    def __init__(self) -> None:
        self._connected = False

    async def connect(self) -> None:
        """PDF connector is always ready."""
        self._connected = True

    async def disconnect(self) -> None:
        """No persistent connection to close."""
        self._connected = False

    async def fetch_documents(self) -> AsyncGenerator[dict, None]:
        """Parse and yield text from PDF files."""
        # TODO: accept file path or bytes, extract text with pypdf
        logger.info("pdf_connector.fetch", message="PDF parsing not yet implemented")
        yield {"content": "", "metadata": {}}

    async def get_metadata(self) -> ConnectorMetadata:
        """Return PDF connector metadata."""
        return ConnectorMetadata(
            name="PDF Connector",
            connector_type="pdf",
            is_connected=self._connected,
        )
