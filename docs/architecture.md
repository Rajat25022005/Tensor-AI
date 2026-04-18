# Architecture Overview

## System Design

TensorAI follows a **layered architecture** with clear separation between data ingestion, memory (graph + vector), agent reasoning, and API presentation.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                             │
│  Dashboard │ Query Interface │ Graph Explorer │ Ingestion │ Settings│
└────────────────────────────┬────────────────────────────────────────┘
                             │  REST / WebSocket
┌────────────────────────────▼────────────────────────────────────────┐
│                     API Layer (FastAPI v1)                          │
│            /health │ /auth │ /query │ /ingest │ /connectors         │
├─────────────────────────────────────────────────────────────────────┤
│                     Middleware                                      │
│              Rate Limiting │ Request Logging │ CORS                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                   Multi-Agent Core                                  │
│                                                                     │
│   ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌───────────┐          │
│   │ Planner  │→│ Retriever  │→ │Executor  │→ │Validator  │          │
│   └──────────┘  └───────────┘  └──────────┘  └───────────┘          │
│                      ↑ retry on validation failure                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                    Memory Layer                                     │
│                                                                     │
│   ┌────────────────┐  ┌──────────────┐  ┌───────────────────┐       │
│   │  Graph Memory  │  │ Vector Store │ │ Hybrid Retriever   │       │
│   │  (Neo4j)       │  │ (ChromaDB /  │ │ graph + vector     │       │
│   │                │  │  Qdrant)     |  │ fusion            │       │
│   └────────────────┘  └──────────────┘  └───────────────────┘       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                   Services                                          │
│   Ingestion Pipeline │ Chunker │ Embedder │ LLM │ Entity Extractor  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                   Connectors                                        │
│              PDF │ Gmail │ Slack │ (extensible)                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                Infrastructure                                       │
│   Docker Compose │ Redis (Celery) │ Neo4j │ ChromaDB │ Ollama       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Ingestion**: Documents arrive via connectors or upload → chunked → embedded → entities extracted → stored in graph + vector store
2. **Query**: User question → Planner decomposes → Retriever pulls from graph + vectors → Executor runs tools → Validator checks → Response
3. **Self-Repair**: If validation fails, the loop retries with refined context from the retriever

## Design Decisions

- **Local-first**: All LLM inference via Ollama — no data leaves the machine
- **Graph + Vector hybrid**: Relational reasoning via Neo4j, semantic similarity via ChromaDB/Qdrant
- **Async-first**: FastAPI + async drivers throughout for high concurrency
- **Celery workers**: Heavy ingestion tasks run in background workers
- **Pluggable connectors**: New data sources implement `BaseConnector` without touching core logic
