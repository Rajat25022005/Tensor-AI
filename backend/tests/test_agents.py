"""Tests for agent modules."""

import pytest

from app.agents.planner import PlannerAgent
from app.agents.validator import ValidatorAgent


@pytest.mark.asyncio
async def test_planner_returns_plan():
    """Planner agent returns a non-empty plan list."""
    planner = PlannerAgent()
    plan = await planner.decompose("What changed in Q3?")
    assert isinstance(plan, list)
    assert len(plan) > 0
    assert "task" in plan[0]


@pytest.mark.asyncio
async def test_validator_passes_valid_result():
    """Validator approves a well-formed result."""
    validator = ValidatorAgent()
    result = {"answer": "Test answer", "sources": [], "reasoning_trace": []}
    is_valid, feedback = await validator.validate("test query", result)
    assert is_valid is True
    assert feedback is None
