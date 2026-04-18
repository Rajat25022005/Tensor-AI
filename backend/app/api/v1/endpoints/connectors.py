"""Connector management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.connectors.registry import ConnectorRegistry
from app.core.dependencies import get_connector_registry
from app.core.logging import logger

router = APIRouter()


class ConnectorStatusResponse(BaseModel):
    """Response model for connector status."""
    name: str
    connector_type: str
    is_connected: bool
    document_count: int


class ConnectorToggleRequest(BaseModel):
    """Request to toggle a connector's connection state."""
    connector_name: str


@router.get("/", summary="List active connectors")
async def list_connectors(
    registry: ConnectorRegistry = Depends(get_connector_registry),
) -> dict:
    """Return metadata for all configured data connectors."""
    metadata_list = await registry.get_all_metadata()

    connectors = []
    for meta in metadata_list:
        connectors.append({
            "name": meta.name,
            "connector_type": meta.connector_type,
            "is_connected": meta.is_connected,
            "document_count": meta.document_count,
        })

    return {"connectors": connectors}


@router.post("/toggle", summary="Toggle connector connection")
async def toggle_connector(
    request: ConnectorToggleRequest,
    registry: ConnectorRegistry = Depends(get_connector_registry),
) -> dict:
    """Connect or disconnect a data connector by name."""
    connector = registry.get(request.connector_name)
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connector '{request.connector_name}' not found. Available: {registry.list_all()}",
        )

    metadata = await connector.get_metadata()

    try:
        if metadata.is_connected:
            await connector.disconnect()
            logger.info("connectors.disconnected", name=request.connector_name)
            return {"message": f"Disconnected '{request.connector_name}'", "is_connected": False}
        else:
            await connector.connect()
            logger.info("connectors.connected", name=request.connector_name)
            return {"message": f"Connected '{request.connector_name}'", "is_connected": True}
    except Exception as exc:
        logger.error("connectors.toggle_failed", name=request.connector_name, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle connector: {str(exc)}",
        )


@router.get("/{connector_name}", summary="Get connector details")
async def get_connector_details(
    connector_name: str,
    registry: ConnectorRegistry = Depends(get_connector_registry),
) -> dict:
    """Return detailed metadata for a specific connector."""
    connector = registry.get(connector_name)
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connector '{connector_name}' not found",
        )

    metadata = await connector.get_metadata()
    return {
        "name": metadata.name,
        "connector_type": metadata.connector_type,
        "is_connected": metadata.is_connected,
        "document_count": metadata.document_count,
    }
