"""Ingestion pipeline — orchestrates document processing end-to-end."""

from dataclasses import dataclass

from app.core.logging import logger
from app.memory.graph_memory import GraphMemory
from app.memory.vector_store import VectorStoreBase
from app.memory.entity_extractor import EntityExtractor
from app.services.chunker import TextChunker
from app.services.embedder import EmbeddingService


@dataclass
class IngestionPipeline:
    """End-to-end document ingestion: chunk → embed → extract → store."""

    chunker: TextChunker
    embedder: EmbeddingService
    extractor: EntityExtractor
    graph_memory: GraphMemory
    vector_store: VectorStoreBase

    async def ingest(self, content: str, filename: str) -> dict:
        """Process a document through the full ingestion pipeline.

        Steps:
            1. Chunk the document into overlapping segments
            2. Generate embeddings for each chunk
            3. Extract entities and relationships via LLM
            4. Store chunks + embeddings in vector store
            5. Store entities + relationships in graph
        """
        logger.info("ingestion.start", filename=filename)

        chunks = self.chunker.chunk(content)
        embeddings = await self.embedder.embed_batch([c["text"] for c in chunks])

        documents = []
        for chunk, embedding in zip(chunks, embeddings):
            documents.append({**chunk, "embedding": embedding})

        await self.vector_store.add_documents(documents)

        all_entities, all_relationships = [], []
        for chunk in chunks:
            entities, relationships = await self.extractor.extract(chunk["text"], filename)
            all_entities.extend(entities)
            all_relationships.extend(relationships)

        for entity in all_entities:
            await self.graph_memory.upsert_entity(entity)
        for rel in all_relationships:
            await self.graph_memory.upsert_relationship(rel)

        logger.info(
            "ingestion.complete",
            filename=filename,
            chunks=len(chunks),
            entities=len(all_entities),
            relationships=len(all_relationships),
        )

        return {
            "chunks_created": len(chunks),
            "entities_extracted": len(all_entities),
            "relationships_extracted": len(all_relationships),
        }
