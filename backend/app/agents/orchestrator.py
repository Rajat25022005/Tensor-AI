"""Agent orchestrator — coordinates the multi-agent reasoning loop."""

from dataclasses import dataclass, field

from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.executor import ExecutorAgent
from app.agents.validator import ValidatorAgent
from app.core.logging import logger


@dataclass
class AgentOrchestrator:
    """Coordinates plan → retrieve → execute → validate loop with self-repair."""

    planner: PlannerAgent = field(default_factory=PlannerAgent)
    retriever: RetrieverAgent = field(default_factory=RetrieverAgent)
    executor: ExecutorAgent = field(default_factory=ExecutorAgent)
    validator: ValidatorAgent = field(default_factory=ValidatorAgent)
    max_retries: int = 2

    async def run(self, query: str, session_id: str | None = None) -> dict:
        """Execute the full agent pipeline for a given query.

        Steps:
            1. Planner decomposes the query into subtasks
            2. Retriever pulls context from graph + vector store
            3. Executor processes subtasks with tools
            4. Validator checks consistency; triggers retry on failure
        """
        logger.info("orchestrator.run.start", query=query[:100], session_id=session_id)

        plan = await self.planner.decompose(query)
        context = await self.retriever.retrieve(plan)

        for attempt in range(1, self.max_retries + 1):
            result = await self.executor.execute(plan, context)
            is_valid, feedback = await self.validator.validate(query, result)

            if is_valid:
                logger.info("orchestrator.run.success", attempt=attempt)
                return result

            logger.warning("orchestrator.run.retry", attempt=attempt, feedback=feedback)
            context = await self.retriever.retrieve(plan, feedback=feedback)

        logger.error("orchestrator.run.exhausted_retries")
        return result
