"""Dashboard stats endpoint — serves aggregate data for the frontend Dashboard."""

from fastapi import APIRouter, Depends

from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase
from app.core.dependencies import get_graph_memory, get_vector_store_dep
from app.core.logging import logger

router = APIRouter()


@router.get("/stats", summary="Get dashboard statistics")
async def get_dashboard_stats(
    graph_memory: GraphMemory = Depends(get_graph_memory),
    vector_store: VectorStoreBase = Depends(get_vector_store_dep),
) -> dict:
    """Return aggregate statistics for the dashboard overview cards.

    Matches the DashboardStats type expected by the frontend.
    """
    graph_nodes = 0
    vector_documents = 0

    # Count graph entities
    try:
        async with graph_memory._driver.session() as session:
            result = await session.run("MATCH (e:Entity) RETURN count(e) AS cnt")
            record = await result.single()
            if record:
                graph_nodes = record["cnt"]
    except Exception as exc:
        logger.warning("dashboard.graph_count_failed", error=str(exc))

    # Count vector store documents
    try:
        vector_documents = await vector_store.count()
    except Exception as exc:
        logger.warning("dashboard.vector_count_failed", error=str(exc))

    # Count relationships for trend metric
    graph_edges = 0
    try:
        async with graph_memory._driver.session() as session:
            result = await session.run("MATCH ()-[r]->() RETURN count(r) AS cnt")
            record = await result.single()
            if record:
                graph_edges = record["cnt"]
    except Exception:
        pass

    return {
        "graphNodes": graph_nodes,
        "graphNodesTrend": graph_edges,
        "agentConfidence": 98.4,  # Placeholder — will be computed from recent query logs
        "validatedTraces": vector_documents,
        "pendingTasks": 0,
    }
