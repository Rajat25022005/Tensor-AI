"""Health-check endpoints with real dependency verification."""

import httpx
from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import logger

router = APIRouter()


@router.get("/", summary="Liveness probe")
async def healthcheck() -> dict[str, str]:
    """Return basic health status — confirms the API process is running."""
    return {"status": "healthy", "service": "tensorai-backend"}


@router.get("/ready", summary="Readiness probe")
async def readiness() -> dict:
    """Verify downstream dependency connectivity before reporting ready.

    Checks: Neo4j, Vector Store (ChromaDB/Qdrant), Ollama.
    """
    checks: dict[str, dict] = {}

    # 1. Check Neo4j
    try:
        from neo4j import AsyncGraphDatabase

        driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
        async with driver.session() as session:
            result = await session.run("RETURN 1 AS n")
            record = await result.single()
            if record and record["n"] == 1:
                checks["neo4j"] = {"status": "connected"}
            else:
                checks["neo4j"] = {"status": "error", "detail": "Unexpected query result"}
        await driver.close()
    except Exception as exc:
        checks["neo4j"] = {"status": "unreachable", "detail": str(exc)[:200]}

    # 2. Check Vector Store
    if settings.VECTOR_STORE_PROVIDER == "chromadb":
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"http://{settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}/api/v1/heartbeat")
                if resp.status_code == 200:
                    checks["vector_store"] = {"status": "connected", "provider": "chromadb"}
                else:
                    checks["vector_store"] = {"status": "error", "provider": "chromadb", "detail": f"HTTP {resp.status_code}"}
        except Exception as exc:
            checks["vector_store"] = {"status": "unreachable", "provider": "chromadb", "detail": str(exc)[:200]}
    else:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}/collections")
                if resp.status_code == 200:
                    checks["vector_store"] = {"status": "connected", "provider": "qdrant"}
                else:
                    checks["vector_store"] = {"status": "error", "provider": "qdrant", "detail": f"HTTP {resp.status_code}"}
        except Exception as exc:
            checks["vector_store"] = {"status": "unreachable", "provider": "qdrant", "detail": str(exc)[:200]}

    # 3. Check Ollama
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                models = [m.get("name", "") for m in resp.json().get("models", [])]
                checks["ollama"] = {"status": "connected", "models": models[:5]}
            else:
                checks["ollama"] = {"status": "error", "detail": f"HTTP {resp.status_code}"}
    except Exception as exc:
        checks["ollama"] = {"status": "unreachable", "detail": str(exc)[:200]}

    # Determine overall readiness
    all_connected = all(c.get("status") == "connected" for c in checks.values())
    overall = "ready" if all_connected else "degraded"

    return {
        "status": overall,
        "checks": checks,
    }
