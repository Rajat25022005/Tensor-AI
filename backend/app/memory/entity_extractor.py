"""Entity extractor — uses LLM to identify entities and relationships from text."""

import hashlib
import json
from dataclasses import dataclass

from app.core.logging import logger
from app.models.domain.graph import Entity, Relationship
from app.services.llm import LLMService

EXTRACTION_SYSTEM_PROMPT = """You are an expert entity and relationship extractor for a business intelligence knowledge graph.

Given a text chunk, extract ALL named entities and relationships between them.

Respond ONLY with valid JSON in this exact format (no extra text):
{
  "entities": [
    {"name": "ENTITY_NAME", "type": "ENTITY_TYPE", "properties": {"key": "value"}}
  ],
  "relationships": [
    {"source": "SOURCE_ENTITY_NAME", "target": "TARGET_ENTITY_NAME", "type": "RELATIONSHIP_TYPE", "confidence": 0.9}
  ]
}

Entity types: PERSON, ORGANIZATION, DOCUMENT, LOCATION, DATE, EVENT, PRODUCT, FINANCIAL, LEGAL, RISK, METRIC, CONCEPT
Relationship types: WORKS_AT, REPORTS_TO, AUTHORED, MENTIONS, RELATES_TO, DEPENDS_ON, CAUSED_BY, PART_OF, MEASURED_BY, SIGNED, APPROVED, AFFECTS

Rules:
- Entity names should be uppercase with underscores (e.g., ACME_CORP)
- Extract at least entities if relationships are unclear
- confidence should be between 0.0 and 1.0
- Keep properties concise and factual
- If no entities are found, return {"entities": [], "relationships": []}"""

EXTRACTION_PROMPT_TEMPLATE = """Extract all entities and relationships from the following text:

---
{text}
---

Return ONLY valid JSON."""


def _make_entity_id(name: str, entity_type: str) -> str:
    """Generate a deterministic ID from entity name and type for graph merging."""
    raw = f"{entity_type}:{name}".lower()
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class EntityExtractor:
    """Extracts structured entities and relationships from unstructured text."""

    llm: LLMService

    async def extract(
        self, text: str, source_document: str | None = None
    ) -> tuple[list[Entity], list[Relationship]]:
        """Extract entities and relationships from a text chunk.

        Args:
            text: The unstructured text to analyze.
            source_document: Optional source document ID for provenance.

        Returns:
            A tuple of (entities, relationships).
        """
        if not text or len(text.strip()) < 20:
            return [], []

        prompt = EXTRACTION_PROMPT_TEMPLATE.format(text=text[:3000])

        try:
            raw_response = await self.llm.generate(
                prompt=prompt,
                system=EXTRACTION_SYSTEM_PROMPT,
            )
            return self._parse_response(raw_response, source_document)
        except Exception as exc:
            logger.warning(
                "entity_extractor.extraction_failed",
                error=str(exc),
                text_preview=text[:80],
            )
            return [], []

    def _parse_response(
        self, raw: str, source_document: str | None
    ) -> tuple[list[Entity], list[Relationship]]:
        """Parse the LLM JSON response into Entity and Relationship objects."""
        # Try to extract JSON from the response (LLM may wrap in markdown)
        json_str = raw.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            logger.warning(
                "entity_extractor.json_parse_failed",
                raw_preview=raw[:200],
            )
            return [], []

        entities: list[Entity] = []
        entity_name_to_id: dict[str, str] = {}

        for raw_entity in data.get("entities", []):
            name = raw_entity.get("name", "").strip().upper().replace(" ", "_")
            entity_type = raw_entity.get("type", "CONCEPT").strip().upper()
            if not name:
                continue

            eid = _make_entity_id(name, entity_type)
            entity_name_to_id[name] = eid

            properties = raw_entity.get("properties", {})
            if source_document:
                properties["source_document"] = source_document

            entities.append(
                Entity(
                    id=eid,
                    name=name,
                    entity_type=entity_type,
                    properties=properties,
                    source_document=source_document,
                )
            )

        relationships: list[Relationship] = []
        for raw_rel in data.get("relationships", []):
            source_name = raw_rel.get("source", "").strip().upper().replace(" ", "_")
            target_name = raw_rel.get("target", "").strip().upper().replace(" ", "_")
            rel_type = raw_rel.get("type", "RELATES_TO").strip().upper()
            confidence = float(raw_rel.get("confidence", 0.8))

            source_id = entity_name_to_id.get(source_name)
            target_id = entity_name_to_id.get(target_name)

            if not source_id or not target_id:
                continue

            relationships.append(
                Relationship(
                    source_id=source_id,
                    target_id=target_id,
                    relation_type=rel_type,
                    confidence=min(max(confidence, 0.0), 1.0),
                    properties={"source_document": source_document} if source_document else {},
                )
            )

        logger.info(
            "entity_extractor.extracted",
            entities=len(entities),
            relationships=len(relationships),
        )

        return entities, relationships
