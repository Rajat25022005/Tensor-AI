"""Validator agent — checks output consistency and triggers self-repair."""

from dataclasses import dataclass


@dataclass
class ValidatorAgent:
    """Validates executor output for consistency, groundedness, and relevance."""

    async def validate(self, query: str, result: dict) -> tuple[bool, str | None]:
        """Validate the executor's result against the original query.

        Args:
            query: The original user query.
            result: The executor's output dict.

        Returns:
            A tuple of (is_valid, feedback_or_none).
        """
        # TODO: LLM-powered consistency and groundedness checks
        return True, None
