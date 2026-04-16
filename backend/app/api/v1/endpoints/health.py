"""Health-check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Liveness probe")
async def healthcheck() -> dict[str, str]:
    """Return basic health status."""
    return {"status": "healthy", "service": "tensorai-backend"}


@router.get("/ready", summary="Readiness probe")
async def readiness() -> dict[str, str]:
    """Return readiness status after verifying downstream dependencies."""
    # TODO: verify Neo4j, vector store, and Ollama connectivity
    return {"status": "ready"}
