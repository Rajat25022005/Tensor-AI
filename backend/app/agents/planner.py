"""Planner agent — decomposes user queries into subtasks."""

from dataclasses import dataclass


@dataclass
class PlannerAgent:
    """Decomposes a complex query into an ordered list of subtasks."""

    async def decompose(self, query: str) -> list[dict]:
        """Break the user query into a plan of subtasks.

        Returns a list of dicts, each with keys: task, tool, description.
        """
        # TODO: LLM-powered decomposition via LangGraph
        return [{"task": "answer", "tool": "retriever", "description": query}]
