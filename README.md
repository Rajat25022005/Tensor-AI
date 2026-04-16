# TensorAI — Autonomous Business Intelligence Platform

> *Your company's second brain. Thinks. Retrieves. Acts.*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat-square)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square)](https://react.dev)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Memory-008CC1?style=flat-square)](https://neo4j.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20Inference-black?style=flat-square)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## Overview

TensorAI is a **multi-agent, graph-augmented AI platform** that helps businesses reason over their own data — documents, emails, databases — without sending anything to the cloud.

Unlike generic RAG chatbots that retrieve flat text chunks, TensorAI builds a **living knowledge graph** of your organization: entities, relationships, events, and time. Agents then plan, retrieve, and act against this graph to answer complex queries and execute multi-step tasks autonomously.

---

## The Problem with Generic RAG

Most enterprise AI tools treat company knowledge as a pile of documents. They miss:

- **Temporal context** — what changed, when, and why
- **Relational structure** — how entities connect across documents
- **Causal chains** — decisions, triggers, and outcomes
- **Persistent memory** — context that survives across sessions

TensorAI is built to close exactly these gaps.

---

## Architecture

```
Business Data Sources
 (PDFs · Emails · Slack · Databases)
              │
     ┌────────▼────────-─┐
     │  Ingestion Layer  │  ← chunking, embedding, deduplication
     └────────┬──────────┘
              │
     ┌────────▼──────────────┐
     │    Graph Memory       │  ← Neo4j: entities, relationships,
     │  (Neo4j + ChromaDB)   │    temporal edges, event nodes
     └────────┬──────────────┘
              │
     ┌────────▼───────────────────────────-─┐
     │         Multi-Agent Core             │
     │                                      │
     │   ┌──────────┐   ┌───────────────┐   │
     │   │  Planner  │   │   Retriever  │   │  ← GraphRAG + vector hybrid
     │   └──────────┘   └───────────────┘   │
     │   ┌──────────┐   ┌───────────────┐   │
     │   │ Executor  │   │   Validator  │   │  ← tool use, self-repair
     │   └──────────┘   └───────────────┘   │
     └────────┬────────────────────────────-┘
              │
     ┌────────▼─────────-─┐
     │   Ollama Backend   │  ← local LLM inference (Mistral / LLaMA 3)
     └────────┬───────────┘
              │
     React Dashboard  /  REST API
```

---

## Key Features

###  Graph-Grounded Memory
Entities and relationships extracted from every ingested document are stored as a property graph in Neo4j. Queries traverse this graph rather than doing flat similarity search — so the system can answer *"What changed in our vendor agreements between Q1 and Q3?"* without hallucinating.

###  Multi-Agent Reasoning Loop
A **Planner** decomposes the user's query into subtasks. A **Retriever** pulls relevant context from both the vector store and the graph. An **Executor** calls tools (summarize, calculate, draft, search). A **Validator** checks the output for consistency before responding. Failed steps trigger self-repair.

###  Local-First Inference
All LLM inference runs via Ollama — no data leaves your machine. Designed for organizations where privacy and data sovereignty are non-negotiable.

###  Pluggable Data Connectors
Ingest from PDFs, Gmail (OAuth), Slack, or any SQL/NoSQL database. New connectors follow a standard interface and can be added without touching core logic.

###  Reasoning Trace UI
Every agent response exposes its full reasoning trace in the React dashboard — which subagents fired, what was retrieved, and why the final answer was chosen. No black boxes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI · Python 3.10+ |
| **Agent Framework** | LangGraph · LangChain |
| **Graph Memory** | Neo4j · Cypher |
| **Vector Store** | ChromaDB / Qdrant |
| **Local LLM** | Ollama (Mistral 7B · LLaMA 3) |
| **Embeddings** | BGE-Large (local) |
| **Frontend** | React 18 · TypeScript · TailwindCSS |
| **Realtime** | Socket.IO |
| **Infrastructure** | Docker · Docker Compose |

---

## Project Structure

```
tensorai/
├── backend/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── retriever.py
│   │   ├── executor.py
│   │   └── validator.py
│   ├── memory/
│   │   ├── graph_builder.py       # entity extraction → Neo4j
│   │   ├── vector_store.py        # ChromaDB ingestion
│   │   └── hybrid_retriever.py    # graph + vector fusion
│   ├── connectors/
│   │   ├── pdf_connector.py
│   │   ├── gmail_connector.py
│   │   └── base_connector.py
│   ├── api/
│   │   └── routes.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── QueryInterface.tsx
│   │   │   ├── ReasoningTrace.tsx
│   │   │   └── GraphViewer.tsx
│   │   └── App.tsx
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Ollama installed locally — pull a model: `ollama pull mistral`
- Neo4j (bundled in docker-compose)

### Run with Docker

```bash
git clone https://github.com/Rajat25022005/tensorai
cd tensorai
cp .env.example .env          # fill in connector credentials
docker-compose up --build
```

Frontend → `http://localhost:3000`  
API docs → `http://localhost:8000/docs`  
Neo4j browser → `http://localhost:7474`

### Manual Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install && npm run dev
```

---

## Roadmap

- [x] Graph memory builder (entity + relation extraction → Neo4j)
- [x] Hybrid retriever (vector + graph traversal)
- [x] Multi-agent loop (plan → retrieve → execute → validate)
- [x] PDF and Gmail connectors
- [x] React dashboard with reasoning trace
- [ ] Slack connector
- [ ] SQL / PostgreSQL connector
- [ ] Role-based access control (multi-tenant)
- [ ] Evaluation harness (faithfulness, groundedness metrics)
- [ ] REST webhook API for external integrations

---

## Motivation

Most enterprise AI tools are wrappers around a single LLM call with document retrieval bolted on. TensorAI is built from different principles: **memory should be structured, reasoning should be transparent, and inference should be local by default.** This project is an attempt to build an AI platform that actually earns trust in production environments.

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change. Please make sure to update tests as appropriate.

---

## Author

**Aditya Rao** — AI/ML Engineer 

---

## License

[MIT](LICENSE) © 2025 Rajat Malik / TensorAI
