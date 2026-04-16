"""Application-wide exception hierarchy."""


class TensorAIError(Exception):
    """Base exception for all TensorAI errors."""

    def __init__(self, message: str = "An unexpected error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class DatabaseConnectionError(TensorAIError):
    """Raised when a database connection fails."""


class GraphQueryError(TensorAIError):
    """Raised when a Neo4j Cypher query fails."""


class VectorStoreError(TensorAIError):
    """Raised when a vector store operation fails."""


class LLMInferenceError(TensorAIError):
    """Raised when the LLM backend fails to respond."""


class ConnectorError(TensorAIError):
    """Raised when a data connector encounters an error."""


class AuthenticationError(TensorAIError):
    """Raised when authentication fails."""


class AuthorizationError(TensorAIError):
    """Raised when a user lacks permission."""


class IngestionError(TensorAIError):
    """Raised when document ingestion fails."""
