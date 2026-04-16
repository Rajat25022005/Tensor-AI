# API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

---

## Endpoints

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health/` | Liveness probe |
| `GET` | `/health/ready` | Readiness probe |

### Authentication

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/login` | Login with email/password → JWT |
| `POST` | `/auth/register` | Register a new account |

#### `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Query

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/query/` | Submit a query to the agent pipeline |

#### `POST /query/`

**Request:**
```json
{
  "question": "What changed in vendor agreements between Q1 and Q3?",
  "session_id": "optional-session-id",
  "max_depth": 3
}
```

**Response:**
```json
{
  "answer": "Based on the indexed documents...",
  "sources": ["vendor_agreement_v2.pdf", "board_minutes_q3.pdf"],
  "reasoning_trace": [
    {
      "agent": "Planner",
      "action": "decompose",
      "input_summary": "What changed...",
      "output_summary": "Identified 2 subtasks",
      "duration_ms": 120.5
    }
  ],
  "confidence": 0.87
}
```

### Ingestion

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ingest/upload` | Upload a file for ingestion |

#### `POST /ingest/upload`

**Request:** `multipart/form-data` with a `file` field.

**Response:**
```json
{
  "filename": "report.pdf",
  "status": "queued",
  "message": "Document received and queued for processing.",
  "document_id": "abc123",
  "chunks_created": null,
  "entities_extracted": null
}
```

### Connectors

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/connectors/` | List configured connectors |
