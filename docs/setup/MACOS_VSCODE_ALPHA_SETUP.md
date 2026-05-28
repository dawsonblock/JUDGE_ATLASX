# macOS + VS Code Alpha Setup

This document covers one clean path for a Mac developer to run the JUDGE_ATLASX alpha locally.

## Prerequisites

| Tool | Required version | Install |
|------|-----------------|---------|
| Python | 3.11.x | `brew install python@3.11` |
| Node | 20.x | `brew install node@20` |
| npm | 10.x | Ships with Node 20 |
| PostgreSQL + PostGIS | 14+ | `brew install postgresql@14 postgis` |
| Redis | 7+ | `brew install redis` |
| Docker | Any current | [docker.com](https://docker.com) |

## Quick start (local, no Docker)

```bash
# 1. Verify environment
python3 scripts/check_local_dev_environment.py

# 2. Copy env files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Start database and Redis
brew services start postgresql@14
brew services start redis

# 4. Backend
cd backend
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 5. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Environment variables

See `.env.example`, `backend/.env.example`, `frontend/.env.example` for all settings.

Every required variable has a comment explaining its purpose. The app boots from `.env.example`
copied to `.env` in development mode.

## Evidence store

The evidence store holds cryptographic snapshots of source material. In development,
a local directory is sufficient:

```bash
mkdir -p ./evidence_store
export JTA_EVIDENCE_STORE_ROOT=./evidence_store
```

Set `JTA_EVIDENCE_STORE_REQUIRED=false` for a DB-only local run without evidence files.

## Redis / queue

By default the queue backend is `inprocess` (no Redis required). Set
`JTA_QUEUE_BACKEND=inprocess` in `.env` to use the in-process mode.

Redis is required for the `redis` rate-limit backend. Switch to memory for local dev:

```bash
JTA_RATE_LIMIT_BACKEND=memory
```

## Running proof checks

```bash
python3 scripts/check_local_dev_environment.py   # environment gate
python3 scripts/check_config_docs_consistency.py  # config/docs sync
python3 backend/scripts/check_proof_consistency.py # proof chain
```

## VS Code workspace

Open the root folder in VS Code. Recommended extensions:

- Python (ms-python.python)
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitLens

Set the Python interpreter to your Python 3.11 venv:

```
Ctrl+Shift+P → Python: Select Interpreter → ./backend/.venv/bin/python
```

## Common issues

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError` on startup | Run `pip install -e ".[dev]"` from `backend/` |
| Frontend blank page | Check `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env` |
| DB connection refused | `brew services start postgresql@14` |
| Migration fails | Run `alembic history` to check chain, then `alembic upgrade head` |
| Rate limit errors | Set `JTA_RATE_LIMIT_BACKEND=memory` in `.env` |

## Alpha warnings

This alpha is **not production software**. Do not:

- Use real personal data in the evidence store
- Deploy publicly without completing proof gates
- Enable `JTA_ENABLE_PUBLIC_PLATFORM=true` before review gates pass

See `docs/status/KNOWN_LIMITATIONS.md` for complete limitations.
