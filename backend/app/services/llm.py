"""LLM service — interface to Ollama for local inference."""

from dataclasses import dataclass
from collections.abc import AsyncGenerator

import httpx

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import LLMInferenceError


@dataclass
class LLMService:
    """Client for Ollama local LLM inference."""

    base_url: str = settings.OLLAMA_BASE_URL
    model: str = settings.OLLAMA_MODEL
    temperature: float = settings.LLM_TEMPERATURE
    max_tokens: int = settings.LLM_MAX_TOKENS

    async def generate(self, prompt: str, system: str | None = None) -> str:
        """Generate a completion from the LLM.

        Args:
            prompt: The user prompt.
            system: Optional system prompt.

        Returns:
            The generated text response.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
                return response.json()["response"]
            except httpx.HTTPError as exc:
                logger.error("llm.generate.failed", error=str(exc))
                raise LLMInferenceError(f"LLM inference failed: {exc}") from exc

    async def stream(self, prompt: str, system: str | None = None) -> AsyncGenerator[str, None]:
        """Stream a completion from the LLM token by token."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                async with client.stream("POST", f"{self.base_url}/api/generate", json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
            except httpx.HTTPError as exc:
                logger.error("llm.stream.failed", error=str(exc))
                raise LLMInferenceError(f"LLM streaming failed: {exc}") from exc
