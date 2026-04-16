"""Entity extractor — uses LLM to identify entities and relationships from text."""

from dataclasses import dataclass

from app.models.domain.graph import Entity, Relationship


@dataclass
class EntityExtractor:
    """Extracts structured entities and relationships from unstructured text."""

    async def extract(self, text: str, source_document: str | None = None) -> tuple[list[Entity], list[Relationship]]:
        """Extract entities and relationships from a text chunk.

        Args:
            text: The unstructured text to analyze.
            source_document: Optional source document ID.

        Returns:
            A tuple of (entities, relationships).
        """
        # TODO: LLM-powered NER and relation extraction
        return [], []
