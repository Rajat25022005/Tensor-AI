"""Connector management endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="List active connectors")
async def list_connectors() -> dict[str, list[str]]:
    """Return a list of configured data connectors."""
    # TODO: wire up ConnectorRegistry
    return {"connectors": ["pdf", "gmail"]}
