"""Validator agent — checks output consistency and triggers self-repair."""

import json
import time
from dataclasses import dataclass

from app.services.llm import LLMService
from app.core.logging import logger

VALIDATION_SYSTEM_PROMPT = """You are a validation agent for a business intelligence system.
Your job is to check whether an answer is consistent, grounded, and relevant to the original query.

Respond ONLY with valid JSON:
{
  "is_valid": true,
  "confidence": 0.85,
  "issues": [],
  "feedback": null
}

If the answer has issues:
{
  "is_valid": false,
  "confidence": 0.3,
  "issues": ["issue 1", "issue 2"],
  "feedback": "Specific guidance on what to re-retrieve or fix"
}

Check for:
1. Relevance — does the answer address the query?
2. Groundedness — is the answer supported by the provided sources?
3. Consistency — are there contradictions?
4. Completeness — are key aspects of the query addressed?"""

VALIDATION_PROMPT = """Validate the following answer against the original query.

Original Query: {query}

Answer: {answer}

Sources cited: {sources}

Is this answer valid? Respond with JSON only."""


@dataclass
class ValidatorAgent:
    """Validates executor output for consistency, groundedness, and relevance."""

    llm: LLMService

    async def validate(self, query: str, result: dict) -> tuple[bool, str | None]:
        """Validate the executor's result against the original query.

        Args:
            query: The original user query.
            result: The executor's output dict with answer, sources, reasoning_trace.

        Returns:
            A tuple of (is_valid, feedback_or_none).
        """
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        confidence = result.get("confidence", 0.0)

        # Quick pass: if answer is clearly empty or an error message, fail fast
        if not answer or len(answer.strip()) < 10:
            return False, "Answer is empty or too short. Re-retrieve with broader context."

        # Quick pass: if confidence is already very high, skip LLM validation
        if confidence >= 0.9 and sources:
            logger.info("validator.quick_pass", confidence=confidence)
            return True, None

        start = time.perf_counter()

        try:
            raw = await self.llm.generate(
                prompt=VALIDATION_PROMPT.format(
                    query=query,
                    answer=answer[:2000],
                    sources=", ".join(sources[:5]) if sources else "none",
                ),
                system=VALIDATION_SYSTEM_PROMPT,
            )

            is_valid, feedback = self._parse_validation(raw)
            duration = (time.perf_counter() - start) * 1000

            logger.info(
                "validator.validate.complete",
                is_valid=is_valid,
                duration_ms=round(duration, 1),
            )
            return is_valid, feedback

        except Exception as exc:
            logger.warning("validator.validate.failed", error=str(exc))
            # On LLM failure, pass through — don't block the pipeline
            return True, None

    def _parse_validation(self, raw: str) -> tuple[bool, str | None]:
        """Parse the LLM validation JSON response."""
        json_str = raw.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(json_str)
            is_valid = bool(data.get("is_valid", True))
            feedback = data.get("feedback")
            return is_valid, feedback
        except json.JSONDecodeError:
            logger.warning("validator.parse_failed", raw_preview=raw[:200])
            # Default to valid if we can't parse
            return True, None
