"""Application lifecycle handlers — startup and shutdown tasks."""

from app.core.logging import logger


async def startup_handler() -> None:
    """Run on application startup.

    Initializes database connections, warms caches, and validates configuration.
    """
    logger.info("lifecycle.startup", message="TensorAI backend starting up")
    # TODO: initialize Neo4j driver pool
    # TODO: initialize vector store client
    # TODO: verify Ollama connectivity
    # TODO: warm embedding model cache


async def shutdown_handler() -> None:
    """Run on application shutdown.

    Gracefully closes connections and flushes buffers.
    """
    logger.info("lifecycle.shutdown", message="TensorAI backend shutting down")
    # TODO: close Neo4j driver
    # TODO: close vector store client
    # TODO: flush log buffers
