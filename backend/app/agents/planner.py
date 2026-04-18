"""Planner agent — decomposes user queries into subtasks using LLM."""

import json
import time
from dataclasses import dataclass

from app.services.llm import LLMService
from app.core.logging import logger

PLANNER_SYSTEM_PROMPT = """You are a query planning agent for a business intelligence system.
Given a user question, decompose it into an ordered list of subtasks.

Respond ONLY with valid JSON in this exact format:
{
  "subtasks": [
    {"task": "brief description", "tool": "tool_name", "description": "detailed description"}
  ]
}

Available tools:
- search_vector: Semantic search across stored documents
- search_graph: Query the knowledge graph for entity relationships
- summarize: Summarize retrieved text
- calculate: Perform calculations on extracted data
- draft: Draft a final answer from gathered context

Rules:
- Order subtasks logically (retrieve before synthesize)
- Use 1-5 subtasks depending on query complexity
- Simple factual queries need fewer steps
- Complex analytical queries need more steps"""

PLANNER_PROMPT = """Decompose the following user query into subtasks:

Query: {query}

Return ONLY valid JSON."""


@dataclass
class PlannerAgent:
    """Decomposes a complex query into an ordered list of subtasks."""

    llm: LLMService

    async def decompose(self, query: str) -> list[dict]:
        """Break the user query into a plan of subtasks.

        Returns a list of dicts, each with keys: task, tool, description.
        """
        start = time.perf_counter()

        try:
            raw = await self.llm.generate(
                prompt=PLANNER_PROMPT.format(query=query),
                system=PLANNER_SYSTEM_PROMPT,
            )

            plan = self._parse_plan(raw, query)
            duration = (time.perf_counter() - start) * 1000

            logger.info(
                "planner.decompose.success",
                subtasks=len(plan),
                duration_ms=round(duration, 1),
            )
            return plan

        except Exception as exc:
            logger.warning("planner.decompose.failed", error=str(exc))
            # Fallback: single retrieval + draft plan
            return [
                {"task": "retrieve", "tool": "search_vector", "description": query},
                {"task": "answer", "tool": "draft", "description": query},
            ]

    def _parse_plan(self, raw: str, original_query: str) -> list[dict]:
        """Parse the LLM JSON response into a subtask list."""
        json_str = raw.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(json_str)
            subtasks = data.get("subtasks", [])
            if not subtasks:
                raise ValueError("Empty subtask list")
            return subtasks
        except (json.JSONDecodeError, ValueError):
            logger.warning("planner.parse_failed", raw_preview=raw[:200])
            return [
                {"task": "retrieve", "tool": "search_vector", "description": original_query},
                {"task": "answer", "tool": "draft", "description": original_query},
            ]
