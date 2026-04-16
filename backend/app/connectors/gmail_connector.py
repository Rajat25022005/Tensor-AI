"""Gmail connector — fetches emails via OAuth2."""

from collections.abc import AsyncGenerator

from app.connectors.base import BaseConnector, ConnectorMetadata
from app.core.logging import logger


class GmailConnector(BaseConnector):
    """Fetches and processes emails from Gmail via OAuth2."""

    def __init__(self, credentials_path: str | None = None) -> None:
        self._credentials_path = credentials_path
        self._connected = False

    async def connect(self) -> None:
        """Authenticate with Gmail API using OAuth2."""
        # TODO: implement OAuth2 flow
        logger.info("gmail_connector.connect", message="OAuth2 not yet implemented")
        self._connected = False

    async def disconnect(self) -> None:
        """Revoke Gmail API session."""
        self._connected = False

    async def fetch_documents(self) -> AsyncGenerator[dict, None]:
        """Yield emails as documents."""
        # TODO: implement Gmail API fetch
        logger.info("gmail_connector.fetch", message="Gmail fetch not yet implemented")
        yield {"content": "", "metadata": {}}

    async def get_metadata(self) -> ConnectorMetadata:
        """Return Gmail connector metadata."""
        return ConnectorMetadata(
            name="Gmail Connector",
            connector_type="gmail",
            is_connected=self._connected,
        )
