"""Graph memory — entity/relationship extraction and Neo4j storage."""

from neo4j import AsyncGraphDatabase

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import GraphQueryError
from app.models.domain.graph import Entity, Relationship


class GraphMemory:
    """Manages the Neo4j knowledge graph: writes entities/relationships, reads subgraphs."""

    def __init__(self) -> None:
        self._driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )

    async def close(self) -> None:
        """Close the Neo4j driver."""
        await self._driver.close()

    async def upsert_entity(self, entity: Entity) -> None:
        """Create or update an entity node in the graph."""
        query = """
        MERGE (e:Entity {id: $id})
        SET e.name = $name, e.type = $entity_type, e += $properties
        """
        async with self._driver.session() as session:
            try:
                await session.run(
                    query,
                    id=entity.id,
                    name=entity.name,
                    entity_type=entity.entity_type,
                    properties=entity.properties,
                )
            except Exception as exc:
                logger.error("graph.upsert_entity.failed", entity_id=entity.id, error=str(exc))
                raise GraphQueryError(f"Failed to upsert entity {entity.id}") from exc

    async def upsert_relationship(self, rel: Relationship) -> None:
        """Create or update a relationship between two entities."""
        query = """
        MATCH (a:Entity {id: $source_id}), (b:Entity {id: $target_id})
        MERGE (a)-[r:RELATES_TO {type: $rel_type}]->(b)
        SET r += $properties, r.confidence = $confidence
        """
        async with self._driver.session() as session:
            try:
                await session.run(
                    query,
                    source_id=rel.source_id,
                    target_id=rel.target_id,
                    rel_type=rel.relation_type,
                    properties=rel.properties,
                    confidence=rel.confidence,
                )
            except Exception as exc:
                logger.error("graph.upsert_relationship.failed", error=str(exc))
                raise GraphQueryError("Failed to upsert relationship") from exc

    async def query_subgraph(self, entity_id: str, depth: int = 2) -> list[dict]:
        """Retrieve a subgraph centered on an entity, up to the given depth."""
        query = """
        MATCH path = (e:Entity {id: $entity_id})-[*1..$depth]-(connected)
        RETURN path
        """
        async with self._driver.session() as session:
            result = await session.run(query, entity_id=entity_id, depth=depth)
            return [record.data() async for record in result]
