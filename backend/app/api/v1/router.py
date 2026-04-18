"""API v1 router — aggregates all domain routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, query, ingest, auth, connectors, graph, dashboard

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(query.router, prefix="/query", tags=["Query"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
api_router.include_router(connectors.router, prefix="/connectors", tags=["Connectors"])
api_router.include_router(graph.router, prefix="/graph", tags=["Graph Explorer"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
