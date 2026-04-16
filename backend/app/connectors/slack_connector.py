"""Slack connector — fetches messages from Slack channels."""

from collections.abc import AsyncGenerator

from app.connectors.base import BaseConnector, ConnectorMetadata
from app.core.logging import logger


class SlackConnector(BaseConnector):
    """Fetches and processes messages from Slack channels."""

    def __init__(self, bot_token: str | None = None) -> None:
        self._bot_token = bot_token
        self._connected = False

    async def connect(self) -> None:
        """Authenticate with Slack API."""
        # TODO: implement Slack Bot API auth
        logger.info("slack_connector.connect", message="Slack auth not yet implemented")
        self._connected = False

    async def disconnect(self) -> None:
        """Close Slack connection."""
        self._connected = False

    async def fetch_documents(self) -> AsyncGenerator[dict, None]:
        """Yield Slack messages as documents."""
        # TODO: implement Slack message fetch
        logger.info("slack_connector.fetch", message="Slack fetch not yet implemented")
        yield {"content": "", "metadata": {}}

    async def get_metadata(self) -> ConnectorMetadata:
        """Return Slack connector metadata."""
        return ConnectorMetadata(
            name="Slack Connector",
            connector_type="slack",
            is_connected=self._connected,
        )
