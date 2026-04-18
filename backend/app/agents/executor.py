"""Executor agent — executes subtasks using tools and LLM."""

import time
from dataclasses import dataclass

from app.agents.tools import ToolRegistry
from app.services.llm import LLMService
from app.core.logging import logger

SYNTHESIS_SYSTEM_PROMPT = """You are an expert business intelligence analyst.
Synthesize a clear, accurate, and well-structured answer from the provided context.
If the context is insufficient, state what is missing rather than fabricating information.
Cite source documents when available."""

SYNTHESIS_PROMPT = """Answer the following question using the retrieved context.

Question: {question}

Retrieved Context:
{context}

Provide a comprehensive, well-structured answer."""


@dataclass
class ExecutorAgent:
    """Executes subtasks by calling tools and synthesizing final answers."""

    llm: LLMService
    tool_registry: ToolRegistry

    async def execute(self, plan: list[dict], context: dict) -> dict:
        """Execute each subtask in the plan using retrieved context.

        Args:
            plan: Ordered list of subtasks from PlannerAgent.
            context: Retrieved context from RetrieverAgent.

        Returns:
            A dict with answer, sources, reasoning_trace, and confidence.
        """
        reasoning_trace = []
        tool_outputs = []
        original_query = context.get("query", "")

        # Execute each subtask
        for step in plan:
            task = step.get("task", "unknown")
            tool_name = step.get("tool", "draft")
            description = step.get("description", "")

            start = time.perf_counter()

            # Build tool kwargs based on tool type
            kwargs = self._build_tool_kwargs(tool_name, description, context, tool_outputs)
            result = await self.tool_registry.call(tool_name, **kwargs)
            tool_outputs.append({"task": task, "tool": tool_name, "result": result})

            duration = (time.perf_counter() - start) * 1000

            # Build reasoning trace entry
            output_summary = self._summarize_tool_output(result)
            reasoning_trace.append({
                "agent": tool_name.upper(),
                "action": task,
                "input_summary": description[:200],
                "output_summary": output_summary[:300],
                "duration_ms": round(duration, 1),
            })

            logger.info(
                "executor.step_complete",
                task=task,
                tool=tool_name,
                duration_ms=round(duration, 1),
            )

        # Synthesize final answer from all tool outputs
        answer, sources, confidence = await self._synthesize(original_query, context, tool_outputs)

        # Add synthesis step to trace
        reasoning_trace.append({
            "agent": "SYNTHESIZER",
            "action": "Final answer synthesis",
            "input_summary": f"Combined {len(tool_outputs)} tool outputs",
            "output_summary": answer[:200],
            "duration_ms": 0.0,
        })

        return {
            "answer": answer,
            "sources": sources,
            "reasoning_trace": reasoning_trace,
            "confidence": confidence,
        }

    def _build_tool_kwargs(
        self, tool_name: str, description: str, context: dict, previous_outputs: list[dict]
    ) -> dict:
        """Build keyword arguments for a tool call based on its type."""
        raw_texts = context.get("raw_texts", [])
        combined_context = "\n\n---\n\n".join(raw_texts[:5])

        if tool_name == "search_vector":
            return {"query": description, "top_k": 5}
        elif tool_name == "search_graph":
            return {"entity_id": description, "depth": 2}
        elif tool_name == "summarize":
            return {"text": combined_context}
        elif tool_name == "draft":
            return {"context": combined_context, "question": description}
        elif tool_name == "calculate":
            return {"expression": description}
        else:
            return {"text": description}

    def _summarize_tool_output(self, result: dict) -> str:
        """Create a brief summary of a tool's output for the reasoning trace."""
        if "error" in result:
            return f"Error: {result['error']}"
        if "summary" in result:
            return result["summary"][:200]
        if "draft" in result:
            return result["draft"][:200]
        if "results" in result:
            count = len(result["results"])
            return f"Retrieved {count} results"
        if "result" in result:
            return str(result["result"])
        return str(result)[:200]

    async def _synthesize(
        self, query: str, context: dict, tool_outputs: list[dict]
    ) -> tuple[str, list[str], float]:
        """Synthesize a final answer from all context and tool outputs."""
        # Gather all text content
        raw_texts = context.get("raw_texts", [])
        draft_texts = []
        for output in tool_outputs:
            r = output.get("result", {})
            if "draft" in r:
                draft_texts.append(r["draft"])
            elif "summary" in r:
                draft_texts.append(r["summary"])
            elif "results" in r and isinstance(r["results"], list):
                for item in r["results"][:3]:
                    if isinstance(item, dict) and "text" in item:
                        draft_texts.append(item["text"])

        # If we already have a draft, use it directly
        if draft_texts:
            answer = draft_texts[-1]
        elif raw_texts:
            # Synthesize from raw context
            combined = "\n\n---\n\n".join(raw_texts[:5])
            try:
                answer = await self.llm.generate(
                    prompt=SYNTHESIS_PROMPT.format(question=query, context=combined),
                    system=SYNTHESIS_SYSTEM_PROMPT,
                )
            except Exception:
                answer = "I was unable to generate a response. The LLM service may be unavailable."
        else:
            answer = "No relevant context was found in the knowledge base to answer this query."

        # Extract sources from vector results
        sources = []
        for doc in context.get("vector_context", []):
            meta = doc.get("metadata", {})
            source = meta.get("source_document") or meta.get("filename") or doc.get("id", "")
            if source and source not in sources:
                sources.append(source)

        # Estimate confidence based on context availability
        confidence = 0.0
        if raw_texts:
            confidence = min(0.5 + 0.1 * len(raw_texts), 0.95)
        if context.get("graph_context"):
            confidence = min(confidence + 0.1, 0.95)

        return answer.strip(), sources[:10], round(confidence, 2)
