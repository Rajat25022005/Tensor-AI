"""Agent tool definitions and callable implementations for the executor."""

from dataclasses import dataclass

from app.core.logging import logger
from app.services.llm import LLMService
from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase
from app.services.embedder import EmbeddingService


@dataclass
class ToolRegistry:
    """Registry of tools available to executor agents."""

    llm: LLMService
    graph_memory: GraphMemory
    vector_store: VectorStoreBase
    embedder: EmbeddingService

    def get_tools(self) -> list[dict]:
        """Return the list of available tools with metadata."""
        return [
            {"name": "summarize", "description": "Summarize a text passage"},
            {"name": "calculate", "description": "Perform a calculation"},
            {"name": "search_graph", "description": "Query the knowledge graph by entity ID"},
            {"name": "search_vector", "description": "Semantic similarity search across documents"},
            {"name": "draft", "description": "Draft a response from retrieved context"},
        ]

    async def call(self, tool_name: str, **kwargs) -> dict:
        """Execute a tool by name and return its result."""
        handler = getattr(self, f"_tool_{tool_name}", None)
        if handler is None:
            logger.warning("tool_registry.unknown_tool", tool=tool_name)
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            return await handler(**kwargs)
        except Exception as exc:
            logger.error("tool_registry.tool_failed", tool=tool_name, error=str(exc))
            return {"error": str(exc)}

    async def _tool_summarize(self, text: str = "", **kwargs) -> dict:
        """Summarize a text passage using the LLM."""
        if not text:
            return {"summary": ""}

        prompt = f"Summarize the following text concisely:\n\n{text[:4000]}"
        summary = await self.llm.generate(
            prompt=prompt,
            system="You are a concise summarizer. Return only the summary, no preamble.",
        )
        return {"summary": summary.strip()}

    async def _tool_search_graph(self, entity_id: str = "", depth: int = 2, **kwargs) -> dict:
        """Query the knowledge graph for a subgraph around an entity."""
        if not entity_id:
            return {"results": []}

        results = await self.graph_memory.query_subgraph(entity_id, depth=depth)
        return {"results": results}

    async def _tool_search_vector(self, query: str = "", top_k: int = 5, **kwargs) -> dict:
        """Perform semantic similarity search across stored documents."""
        if not query:
            return {"results": []}

        embedding = await self.embedder.embed(query)
        results = await self.vector_store.search(embedding, top_k=top_k)
        return {"results": results}

    async def _tool_draft(self, context: str = "", question: str = "", **kwargs) -> dict:
        """Draft a response using context and the original question."""
        prompt = f"""Based on the following context, answer the question.

Context:
{context[:4000]}

Question: {question}

Provide a clear, well-structured answer grounded in the context."""

        answer = await self.llm.generate(
            prompt=prompt,
            system="You are an expert analyst. Answer based strictly on the provided context. If the context is insufficient, say so.",
        )
        return {"draft": answer.strip()}

    async def _tool_calculate(self, expression: str = "", **kwargs) -> dict:
        """Safely evaluate a mathematical expression."""
        if not expression:
            return {"result": None, "error": "No expression provided"}

        try:
            # Safe eval — only allow basic math operations
            allowed_chars = set("0123456789+-*/().% ")
            if not all(c in allowed_chars for c in expression):
                return {"result": None, "error": "Expression contains disallowed characters"}

            result = eval(expression)  # noqa: S307
            return {"result": float(result)}
        except Exception as exc:
            return {"result": None, "error": str(exc)}
