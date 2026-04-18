"""Graph explorer endpoint — serves subgraph data for the frontend GraphExplorer."""

from fastapi import APIRouter, Depends, Query

from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase
from app.core.dependencies import get_graph_memory, get_vector_store_dep
from app.core.logging import logger

router = APIRouter()


@router.get("/{entity_id}", summary="Get subgraph for an entity")
async def get_subgraph(
    entity_id: str,
    depth: int = Query(default=2, ge=1, le=5, description="Traversal depth"),
    graph_memory: GraphMemory = Depends(get_graph_memory),
) -> dict:
    """Retrieve a subgraph centered on the given entity ID.

    Returns nodes and edges in a format the frontend GraphExplorer can render.
    """
    logger.info("graph.subgraph.request", entity_id=entity_id, depth=depth)

    try:
        raw_paths = await graph_memory.query_subgraph(entity_id, depth=depth)

        # Transform Neo4j path results into frontend-friendly nodes + edges
        nodes_map: dict[str, dict] = {}
        edges: list[dict] = []

        for record in raw_paths:
            path = record.get("path")
            if not path:
                continue

            # Extract nodes from path
            if hasattr(path, "nodes"):
                for node in path.nodes:
                    nid = node.get("id", str(node.id))
                    if nid not in nodes_map:
                        nodes_map[nid] = {
                            "id": nid,
                            "name": node.get("name", nid),
                            "type": node.get("type", node.get("entity_type", "ENTITY")),
                            "properties": dict(node),
                        }

                # Extract relationships from path
                for rel in path.relationships:
                    edges.append({
                        "source": rel.start_node.get("id", str(rel.start_node.id)),
                        "target": rel.end_node.get("id", str(rel.end_node.id)),
                        "label": rel.get("type", type(rel).__name__),
                        "confidence": rel.get("confidence", 1.0),
                    })

        nodes = list(nodes_map.values())

        logger.info(
            "graph.subgraph.complete",
            entity_id=entity_id,
            nodes=len(nodes),
            edges=len(edges),
        )

        return {"nodes": nodes, "edges": edges}

    except Exception as exc:
        logger.warning("graph.subgraph.failed", entity_id=entity_id, error=str(exc))
        # Return empty graph rather than erroring — frontend handles gracefully
        return {"nodes": [], "edges": []}


@router.get("/", summary="Get graph overview stats")
async def get_graph_stats(
    graph_memory: GraphMemory = Depends(get_graph_memory),
    vector_store: VectorStoreBase = Depends(get_vector_store_dep),
) -> dict:
    """Return high-level graph and vector store statistics."""
    graph_count = 0
    vector_count = 0

    try:
        # Count graph entities
        async with graph_memory._driver.session() as session:
            result = await session.run("MATCH (e:Entity) RETURN count(e) AS cnt")
            record = await result.single()
            if record:
                graph_count = record["cnt"]
    except Exception:
        pass

    try:
        vector_count = await vector_store.count()
    except Exception:
        pass

    return {
        "graph_nodes": graph_count,
        "vector_documents": vector_count,
    }
