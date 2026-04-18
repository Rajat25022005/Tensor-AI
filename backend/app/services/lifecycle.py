"""Application lifecycle handlers — startup and shutdown tasks."""

import httpx

from app.core.config import settings
from app.core.logging import logger
from app.core.dependencies import init_services, close_services


async def startup_handler() -> None:
    """Run on application startup.

    Initializes service singletons, verifies downstream connectivity.
    """
    logger.info("lifecycle.startup", message="TensorAI backend starting up")

    # Initialize all service singletons (graph, vector, LLM, embedder, etc.)
    init_services()
    logger.info("lifecycle.services_initialized")

    # Verify Ollama connectivity (non-blocking — warn if unreachable)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                logger.info("lifecycle.ollama_connected", available_models=models)
            else:
                logger.warning("lifecycle.ollama_unhealthy", status=resp.status_code)
    except Exception as exc:
        logger.warning(
            "lifecycle.ollama_unreachable",
            url=settings.OLLAMA_BASE_URL,
            error=str(exc),
            message="Ollama is not reachable. LLM features will fail until it's available.",
        )

    logger.info("lifecycle.startup_complete")


async def shutdown_handler() -> None:
    """Run on application shutdown.

    Gracefully closes connections and flushes buffers.
    """
    logger.info("lifecycle.shutdown", message="TensorAI backend shutting down")

    await close_services()

    logger.info("lifecycle.shutdown_complete")
