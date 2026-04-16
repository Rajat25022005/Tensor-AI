"""Hybrid retriever — fuses graph traversal and vector similarity results."""

from dataclasses import dataclass

from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase


@dataclass
class HybridRetriever:
    """Combines graph and vector retrieval with re-ranking."""

    graph_memory: GraphMemory
    vector_store: VectorStoreBase

    async def retrieve(
        self,
        query_embedding: list[float],
        entity_ids: list[str] | None = None,
        top_k: int = 10,
        graph_depth: int = 2,
    ) -> dict:
        """Perform hybrid retrieval.

        1. Vector similarity search for top_k chunks
        2. Graph traversal from seed entities
        3. Merge and re-rank results

        Returns a dict with vector_results and graph_results.
        """
        vector_results = await self.vector_store.search(query_embedding, top_k=top_k)

        graph_results = []
        if entity_ids:
            for eid in entity_ids:
                subgraph = await self.graph_memory.query_subgraph(eid, depth=graph_depth)
                graph_results.extend(subgraph)

        return {
            "vector_results": vector_results,
            "graph_results": graph_results,
        }
