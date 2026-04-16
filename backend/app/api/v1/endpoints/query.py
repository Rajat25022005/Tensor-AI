"""Query endpoint — accepts user questions and returns agent-processed answers."""

from fastapi import APIRouter, Depends

from app.models.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/", response_model=QueryResponse, summary="Submit a query")
async def submit_query(request: QueryRequest) -> QueryResponse:
    """Accept a user query and run the multi-agent reasoning loop."""
    # TODO: wire up AgentOrchestrator
    return QueryResponse(
        answer="Agent pipeline not yet connected.",
        sources=[],
        reasoning_trace=[],
    )
