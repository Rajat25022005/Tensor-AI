"""Tests for health endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient):
    """Health endpoint returns 200 with healthy status."""
    response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "tensorai-backend"


@pytest.mark.asyncio
async def test_readiness(client: AsyncClient):
    """Readiness endpoint returns 200 with ready status."""
    response = await client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
