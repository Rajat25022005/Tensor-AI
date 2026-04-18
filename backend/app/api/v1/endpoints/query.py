"""Query endpoint — accepts user questions and returns agent-processed answers."""

import time

from fastapi import APIRouter, Depends

from app.models.schemas.query import QueryRequest, QueryResponse, ReasoningStep
from app.agents.orchestrator import AgentOrchestrator
from app.core.dependencies import get_orchestrator
from app.core.logging import logger

router = APIRouter()


@router.post("/", response_model=QueryResponse, summary="Submit a query")
async def submit_query(
    request: QueryRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
) -> QueryResponse:
    """Accept a user query and run the multi-agent reasoning loop."""
    logger.info("query.submit", question=request.question[:100], session_id=request.session_id)

    start = time.perf_counter()
    result = await orchestrator.run(
        query=request.question,
        session_id=request.session_id,
    )
    total_ms = (time.perf_counter() - start) * 1000

    # Convert raw trace dicts to ReasoningStep models
    trace = []
    for step in result.get("reasoning_trace", []):
        trace.append(
            ReasoningStep(
                agent=step.get("agent", "UNKNOWN"),
                action=step.get("action", ""),
                input_summary=step.get("input_summary", ""),
                output_summary=step.get("output_summary", ""),
                duration_ms=step.get("duration_ms", 0.0),
            )
        )

    logger.info("query.complete", total_ms=round(total_ms, 1), confidence=result.get("confidence", 0))

    return QueryResponse(
        answer=result.get("answer", "No answer generated."),
        sources=result.get("sources", []),
        reasoning_trace=trace,
        confidence=result.get("confidence", 0.0),
    )
