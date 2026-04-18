"""Agent orchestrator — coordinates the multi-agent reasoning loop."""

import time
from dataclasses import dataclass, field

from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.executor import ExecutorAgent
from app.agents.validator import ValidatorAgent
from app.agents.tools import ToolRegistry
from app.services.llm import LLMService
from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase
from app.services.embedder import EmbeddingService
from app.core.logging import logger


@dataclass
class AgentOrchestrator:
    """Coordinates plan → retrieve → execute → validate loop with self-repair."""

    llm: LLMService
    graph_memory: GraphMemory
    vector_store: VectorStoreBase
    embedder: EmbeddingService
    max_retries: int = 2

    def __post_init__(self) -> None:
        """Initialize sub-agents with shared dependencies."""
        self.planner = PlannerAgent(llm=self.llm)
        self.retriever = RetrieverAgent(
            graph_memory=self.graph_memory,
            vector_store=self.vector_store,
            embedder=self.embedder,
        )
        self.tool_registry = ToolRegistry(
            llm=self.llm,
            graph_memory=self.graph_memory,
            vector_store=self.vector_store,
            embedder=self.embedder,
        )
        self.executor = ExecutorAgent(llm=self.llm, tool_registry=self.tool_registry)
        self.validator = ValidatorAgent(llm=self.llm)

    async def run(self, query: str, session_id: str | None = None) -> dict:
        """Execute the full agent pipeline for a given query.

        Steps:
            1. Planner decomposes the query into subtasks
            2. Retriever pulls context from graph + vector store
            3. Executor processes subtasks with tools
            4. Validator checks consistency; triggers retry on failure
        """
        pipeline_start = time.perf_counter()
        logger.info("orchestrator.run.start", query=query[:100], session_id=session_id)

        # Step 1: Plan
        plan_start = time.perf_counter()
        plan = await self.planner.decompose(query)
        plan_duration = (time.perf_counter() - plan_start) * 1000

        # Step 2: Retrieve
        retrieve_start = time.perf_counter()
        context = await self.retriever.retrieve(plan)
        retrieve_duration = (time.perf_counter() - retrieve_start) * 1000

        # Steps 3-4: Execute and validate with retry loop
        result = {}
        for attempt in range(1, self.max_retries + 1):
            exec_start = time.perf_counter()
            result = await self.executor.execute(plan, context)
            exec_duration = (time.perf_counter() - exec_start) * 1000

            val_start = time.perf_counter()
            is_valid, feedback = await self.validator.validate(query, result)
            val_duration = (time.perf_counter() - val_start) * 1000

            # Inject orchestrator-level timing into the trace
            if attempt == 1:
                orchestrator_trace = [
                    {
                        "agent": "PLANNER",
                        "action": f"Decomposed into {len(plan)} subtasks",
                        "input_summary": query[:200],
                        "output_summary": ", ".join(s.get("task", "") for s in plan),
                        "duration_ms": round(plan_duration, 1),
                    },
                    {
                        "agent": "RETRIEVER",
                        "action": "Hybrid graph + vector retrieval",
                        "input_summary": f"{len(plan)} subtasks",
                        "output_summary": f"{len(context.get('vector_context', []))} vector + {len(context.get('graph_context', []))} graph results",
                        "duration_ms": round(retrieve_duration, 1),
                    },
                ]
                existing_trace = result.get("reasoning_trace", [])
                result["reasoning_trace"] = orchestrator_trace + existing_trace

            if is_valid:
                total_duration = (time.perf_counter() - pipeline_start) * 1000
                logger.info(
                    "orchestrator.run.success",
                    attempt=attempt,
                    total_ms=round(total_duration, 1),
                )
                return result

            logger.warning(
                "orchestrator.run.retry",
                attempt=attempt,
                feedback=feedback,
            )
            # Re-retrieve with validator feedback
            context = await self.retriever.retrieve(plan, feedback=feedback)

        total_duration = (time.perf_counter() - pipeline_start) * 1000
        logger.error(
            "orchestrator.run.exhausted_retries",
            total_ms=round(total_duration, 1),
        )
        return result
