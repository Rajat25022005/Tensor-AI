"""Retriever agent — hybrid graph + vector retrieval."""

import time
from dataclasses import dataclass

from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase
from app.services.embedder import EmbeddingService
from app.core.logging import logger


@dataclass
class RetrieverAgent:
    """Performs hybrid retrieval: graph traversal + vector similarity search."""

    graph_memory: GraphMemory
    vector_store: VectorStoreBase
    embedder: EmbeddingService

    async def retrieve(
        self, plan: list[dict], feedback: str | None = None
    ) -> dict:
        """Retrieve relevant context for the plan from graph and vector store.

        Args:
            plan: The decomposed subtask plan from PlannerAgent.
            feedback: Optional validator feedback for re-retrieval on retry.

        Returns:
            A dict containing graph_context, vector_context, and raw_texts.
        """
        start = time.perf_counter()

        # Build a combined query from all subtask descriptions
        descriptions = [step.get("description", "") for step in plan]
        combined_query = " ".join(descriptions)

        if feedback:
            combined_query = f"{combined_query} Additional focus: {feedback}"

        # 1. Vector similarity search
        vector_context = []
        try:
            query_embedding = await self.embedder.embed(combined_query)
            vector_context = await self.vector_store.search(query_embedding, top_k=8)
        except Exception as exc:
            logger.warning("retriever.vector_search_failed", error=str(exc))

        # 2. Graph traversal — extract entity IDs from vector results metadata
        graph_context = []
        try:
            entity_ids = set()
            for doc in vector_context:
                meta = doc.get("metadata", {})
                if "entity_id" in meta:
                    entity_ids.add(meta["entity_id"])

            for eid in list(entity_ids)[:5]:
                subgraph = await self.graph_memory.query_subgraph(eid, depth=2)
                graph_context.extend(subgraph)
        except Exception as exc:
            logger.warning("retriever.graph_search_failed", error=str(exc))

        # 3. Compile raw texts for downstream agents
        raw_texts = [doc.get("text", "") for doc in vector_context if doc.get("text")]

        duration = (time.perf_counter() - start) * 1000
        logger.info(
            "retriever.retrieve.complete",
            vector_results=len(vector_context),
            graph_results=len(graph_context),
            duration_ms=round(duration, 1),
        )

        return {
            "graph_context": graph_context,
            "vector_context": vector_context,
            "raw_texts": raw_texts,
            "query": combined_query,
        }
