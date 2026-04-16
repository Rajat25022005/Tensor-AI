<p align="center">
  <strong>T E N S O R A I</strong>
</p>

<h3 align="center">Autonomous Business Intelligence Platform</h3>

<p align="center">
  <em>Your company's second brain. Thinks. Retrieves. Acts.</em>
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://react.dev"><img src="https://img.shields.io/badge/React_18-TypeScript-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" /></a>
  <a href="https://neo4j.com"><img src="https://img.shields.io/badge/Neo4j-Graph_Memory-4581C3?style=for-the-badge&logo=neo4j&logoColor=white" alt="Neo4j" /></a>
  <a href="https://ollama.com"><img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-F7DF1E?style=for-the-badge" alt="License" /></a>
</p>

---

## Overview

TensorAI is a **multi-agent, graph-augmented AI platform** that helps businesses reason over their own data — documents, emails, databases — without sending anything to the cloud.

Unlike generic RAG chatbots that retrieve flat text chunks, TensorAI builds a **living knowledge graph** of your organization: entities, relationships, events, and time. Agents then plan, retrieve, and act against this graph to answer complex queries and execute multi-step tasks autonomously.

---

## The Problem with Generic RAG

Most enterprise AI tools treat company knowledge as a pile of documents. They miss:

| Gap | What's Lost |
|-----|-------------|
| **Temporal context** | What changed, when, and why |
| **Relational structure** | How entities connect across documents |
| **Causal chains** | Decisions, triggers, and outcomes |
| **Persistent memory** | Context that survives across sessions |

TensorAI is built to close exactly these gaps.

---

## Architecture

```
Business Data Sources
 (PDFs · Emails · Slack · Databases)
              │
     ┌────────▼──────────┐
     │  Ingestion Layer   │  ← chunking, embedding, entity extraction
     └────────┬───────────┘
              │
     ┌────────▼──────────────┐
     │    Memory Layer       │
     │  Neo4j (Graph)        │  ← entities, relationships,
     │  ChromaDB / Qdrant    │    temporal edges, event nodes
     │  (Vectors)            │
     └────────┬──────────────┘
              │
     ┌────────▼─────────────────────────────┐
     │         Multi-Agent Core             │
     │                                      │
     │   Planner → Retriever → Executor     │
     │                  ↑          │        │
     │                  └─ Validator ◄──────┘│
     │            (self-repair on failure)   │
     └────────┬─────────────────────────────┘
              │
     ┌────────▼────────────┐
     │   Ollama Backend    │  ← local LLM inference
     └────────┬────────────┘
              │
     React Dashboard  /  REST + WebSocket API
```

> **Full architecture docs**: [`docs/architecture.md`](docs/architecture.md)

---

## Key Features

### 🧠 Graph-Grounded Memory
Entities and relationships extracted from every ingested document are stored as a property graph in Neo4j. Queries traverse this graph rather than doing flat similarity search — so the system can answer *"What changed in our vendor agreements between Q1 and Q3?"* without hallucinating.

### 🔄 Multi-Agent Reasoning Loop
A **Planner** decomposes the user's query into subtasks. A **Retriever** pulls relevant context from both the vector store and the graph. An **Executor** calls tools (summarize, calculate, draft, search). A **Validator** checks the output for consistency before responding. Failed steps trigger self-repair.

### 🔒 Local-First Inference
All LLM inference runs via Ollama — no data leaves your machine. Designed for organizations where privacy and data sovereignty are non-negotiable.

### 🔌 Pluggable Data Connectors
Ingest from PDFs, Gmail (OAuth), Slack, or any SQL/NoSQL database. New connectors follow a standard interface (`BaseConnector`) and can be added without touching core logic.

### 🔍 Reasoning Trace UI
Every agent response exposes its full reasoning trace in the React dashboard — which subagents fired, what was retrieved, and why the final answer was chosen. No black boxes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI · Python 3.10+ · Pydantic v2 |
| **Agent Framework** | LangGraph · LangChain |
| **Graph Memory** | Neo4j 5 · Cypher |
| **Vector Store** | ChromaDB / Qdrant (pluggable) |
| **Local LLM** | Ollama (Mistral 7B · LLaMA 3) |
| **Embeddings** | BGE-Large (local, 1024-dim) |
| **Frontend** | React 18 · TypeScript · Vite · Zustand |
| **Realtime** | Socket.IO |
| **Task Queue** | Celery · Redis |
| **Infrastructure** | Docker Compose · GitHub Actions CI |

---

## Project Structure

```
tensorai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py           # login, register
│   │   │       │   ├── connectors.py     # connector management
│   │   │       │   ├── health.py         # liveness + readiness probes
│   │   │       │   ├── ingest.py         # document upload
│   │   │       │   └── query.py          # query submission
│   │   │       └── router.py             # API v1 router aggregation
│   │   ├── agents/
│   │   │   ├── orchestrator.py           # plan→retrieve→execute→validate loop
│   │   │   ├── planner.py               # query decomposition
│   │   │   ├── retriever.py             # hybrid graph+vector retrieval
│   │   │   ├── executor.py              # tool execution
│   │   │   ├── validator.py             # output consistency checks
│   │   │   └── tools.py                 # tool registry
│   │   ├── connectors/
│   │   │   ├── base.py                  # BaseConnector interface
│   │   │   ├── pdf_connector.py
│   │   │   ├── gmail_connector.py
│   │   │   ├── slack_connector.py
│   │   │   └── registry.py             # connector registry
│   │   ├── core/
│   │   │   ├── config.py               # pydantic-settings config
│   │   │   ├── dependencies.py          # DI providers
│   │   │   ├── exceptions.py            # exception hierarchy
│   │   │   ├── logging.py              # structlog setup
│   │   │   └── security.py             # JWT + bcrypt
│   │   ├── memory/
│   │   │   ├── entity_extractor.py      # LLM-powered NER
│   │   │   ├── graph_memory.py          # Neo4j client
│   │   │   ├── hybrid_retriever.py      # graph+vector fusion
│   │   │   └── vector_store.py          # ChromaDB/Qdrant abstraction
│   │   ├── middleware/
│   │   │   ├── logging.py              # request logging
│   │   │   └── rate_limit.py           # rate limiter
│   │   ├── models/
│   │   │   ├── domain/
│   │   │   │   └── graph.py            # Entity, Relationship, Document
│   │   │   └── schemas/
│   │   │       ├── auth.py             # LoginRequest, TokenResponse
│   │   │       ├── ingest.py           # IngestResponse
│   │   │       └── query.py            # QueryRequest/Response
│   │   ├── services/
│   │   │   ├── chunker.py             # text chunking
│   │   │   ├── embedder.py            # embedding generation
│   │   │   ├── ingestion.py           # end-to-end ingestion pipeline
│   │   │   ├── lifecycle.py           # startup/shutdown handlers
│   │   │   └── llm.py                 # Ollama client
│   │   ├── workers/
│   │   │   ├── celery_app.py          # Celery configuration
│   │   │   └── tasks.py              # background ingestion tasks
│   │   └── main.py                    # FastAPI app entrypoint
│   ├── tests/
│   │   ├── conftest.py                # shared fixtures
│   │   ├── test_agents.py
│   │   ├── test_chunker.py
│   │   └── test_health.py
│   ├── Dockerfile
│   └── pyproject.toml                 # Python deps + tool config
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── graph/
│   │   │   │   └── GraphViewer.tsx     # force-directed graph viz
│   │   │   ├── ingestion/
│   │   │   │   └── FileUpload.tsx      # drag-and-drop upload
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Layout.tsx
│   │   │   │   └── Sidebar.tsx
│   │   │   └── query/
│   │   │       ├── QueryInterface.tsx  # query input
│   │   │       └── ReasoningTrace.tsx  # agent trace display
│   │   ├── hooks/
│   │   │   └── useApi.ts              # data fetching + debounce
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── GraphExplorer.tsx
│   │   │   ├── IngestionPage.tsx
│   │   │   ├── QueryPage.tsx
│   │   │   └── SettingsPage.tsx
│   │   ├── services/
│   │   │   ├── api.ts                 # axios client + interceptors
│   │   │   └── socket.ts             # Socket.IO client
│   │   ├── stores/
│   │   │   ├── graphStore.ts          # Zustand graph state
│   │   │   └── queryStore.ts          # Zustand query state
│   │   ├── styles/
│   │   │   └── index.css              # design system + CSS variables
│   │   ├── types/
│   │   │   └── index.ts               # shared TypeScript types
│   │   ├── utils/
│   │   │   └── helpers.ts             # utility functions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── docs/
│   ├── api.md                         # API reference
│   ├── architecture.md                # system design docs
│   └── CONTRIBUTING.md                # contribution guidelines
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI pipeline
│
├── .env.example                       # environment variable template
├── .gitignore
├── docker-compose.yml                 # full-stack orchestration
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Ollama** installed locally — pull a model:
  ```bash
  ollama pull mistral
  ```

### Quick Start (Docker)

```bash
git clone https://github.com/Aditya36999/Tensor-AI.git
cd Tensor-AI
cp .env.example .env          # configure your settings
docker compose up --build
```

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **API Docs** | http://localhost:8000/docs |
| **Neo4j Browser** | http://localhost:7474 |
| **ChromaDB** | http://localhost:8100 |

### Manual Setup (Development)

```bash
# 1. Start infrastructure
docker compose up neo4j chromadb redis -d

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

# 3. Frontend (in a new terminal)
cd frontend
npm install && npm run dev
```

### Running Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run lint && npm run build
```

---

## Environment Variables

See [`.env.example`](.env.example) for all configurable variables. Key settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | `development` / `production` |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection URI |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `mistral` | Default LLM model |
| `VECTOR_STORE_PROVIDER` | `chromadb` | `chromadb` or `qdrant` |

---

## Roadmap

- [x] Graph memory builder (entity + relation extraction → Neo4j)
- [x] Hybrid retriever (vector + graph traversal)
- [x] Multi-agent loop (plan → retrieve → execute → validate)
- [x] PDF and Gmail connectors
- [x] React dashboard with reasoning trace
- [x] Production project structure with CI/CD
- [ ] Slack connector (scaffold complete)
- [ ] SQL / PostgreSQL connector
- [ ] Role-based access control (multi-tenant)
- [ ] Evaluation harness (faithfulness, groundedness metrics)
- [ ] REST webhook API for external integrations
- [ ] Kubernetes deployment manifests

---

## API Reference

Full API documentation is available at:
- **Interactive**: http://localhost:8000/docs (Swagger UI)
- **Static**: [`docs/api.md`](docs/api.md)

---

## Contributing

Pull requests are welcome. See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for development setup, code quality standards, and git workflow.

---

## Motivation

Most enterprise AI tools are wrappers around a single LLM call with document retrieval bolted on. TensorAI is built from different principles: **memory should be structured, reasoning should be transparent, and inference should be local by default.** This project is an attempt to build an AI platform that actually earns trust in production environments.

---

## Authors

**Aditya Rao** — AI/ML Engineer

---

## License

[MIT](LICENSE) © 2026 TensorAI
