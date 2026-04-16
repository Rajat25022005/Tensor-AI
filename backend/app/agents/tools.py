"""Agent tool definitions for the executor."""

from dataclasses import dataclass


@dataclass
class ToolRegistry:
    """Registry of tools available to executor agents."""

    def get_tools(self) -> list[dict]:
        """Return the list of available tools with metadata."""
        return [
            {"name": "summarize", "description": "Summarize a text passage"},
            {"name": "calculate", "description": "Perform a calculation"},
            {"name": "search_graph", "description": "Query the knowledge graph"},
            {"name": "search_vector", "description": "Semantic similarity search"},
            {"name": "draft", "description": "Draft a response from context"},
        ]
