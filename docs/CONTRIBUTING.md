# Contributing to TensorAI

Thank you for your interest in contributing to TensorAI! This document provides guidelines for contributing to this project.

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 20+
- Docker & Docker Compose
- Ollama (with a model pulled: `ollama pull mistral`)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running Locally

```bash
# Start infrastructure services
docker compose up neo4j chromadb redis -d

# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

## Code Quality

### Python (Backend)

- **Linter**: [Ruff](https://docs.astral.sh/ruff/)
- **Type checker**: [mypy](https://mypy-lang.org/) (strict mode)
- **Tests**: [pytest](https://docs.pytest.org/) with pytest-asyncio

```bash
cd backend
ruff check .          # lint
ruff format .         # format
mypy app/             # type check
pytest                # test
```

### TypeScript (Frontend)

- **Linter**: ESLint with TypeScript plugin
- **Type checker**: `tsc --noEmit`

```bash
cd frontend
npm run lint          # lint
npm run type-check    # type check
npm run build         # build check
```

## Git Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit with conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
4. Push and open a Pull Request against `develop`

## Adding a New Connector

1. Create `backend/app/connectors/your_connector.py`
2. Implement `BaseConnector` (see `base.py`)
3. Register it in `ConnectorRegistry` (`registry.py`)
4. Add tests in `backend/tests/test_connectors.py`

## Code Review Checklist

- [ ] Code passes lint and type checks
- [ ] New functionality has tests
- [ ] Documentation updated if needed
- [ ] No sensitive data in commits
