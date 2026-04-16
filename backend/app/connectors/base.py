"""Base connector interface — all data connectors must implement this."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import AsyncGenerator


@dataclass
class ConnectorMetadata:
    """Metadata about a connected data source."""

    name: str
    connector_type: str
    is_connected: bool = False
    document_count: int = 0


class BaseConnector(ABC):
    """Abstract base class for all data source connectors."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the data source."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the connection to the data source."""
        ...

    @abstractmethod
    async def fetch_documents(self) -> AsyncGenerator[dict, None]:
        """Yield documents from the data source one at a time."""
        ...

    @abstractmethod
    async def get_metadata(self) -> ConnectorMetadata:
        """Return connector status and metadata."""
        ...
