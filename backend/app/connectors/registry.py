"""Connector registry — manages all available data connectors."""

from app.connectors.base import BaseConnector, ConnectorMetadata
from app.connectors.pdf_connector import PDFConnector
from app.connectors.gmail_connector import GmailConnector
from app.connectors.slack_connector import SlackConnector


class ConnectorRegistry:
    """Central registry for managing data source connectors."""

    def __init__(self) -> None:
        self._connectors: dict[str, BaseConnector] = {
            "pdf": PDFConnector(),
            "gmail": GmailConnector(),
            "slack": SlackConnector(),
        }

    def get(self, name: str) -> BaseConnector | None:
        """Get a connector by name."""
        return self._connectors.get(name)

    def list_all(self) -> list[str]:
        """List all registered connector names."""
        return list(self._connectors.keys())

    def register(self, name: str, connector: BaseConnector) -> None:
        """Register a new connector."""
        self._connectors[name] = connector

    async def get_all_metadata(self) -> list[ConnectorMetadata]:
        """Get metadata for all registered connectors."""
        return [await c.get_metadata() for c in self._connectors.values()]
