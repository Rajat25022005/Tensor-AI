"""Retriever agent — hybrid graph + vector retrieval."""

from dataclasses import dataclass


@dataclass
class RetrieverAgent:
    """Performs hybrid retrieval: graph traversal + vector similarity search."""

    async def retrieve(
        self, plan: list[dict], feedback: str | None = None
    ) -> dict:
        """Retrieve relevant context for the plan from graph and vector store.

        Args:
            plan: The decomposed subtask plan from PlannerAgent.
            feedback: Optional validator feedback for re-retrieval on retry.

        Returns:
            A dict containing graph_context and vector_context.
        """
        # TODO: wire up GraphMemory and VectorStore
        return {"graph_context": [], "vector_context": []}
