# Project Context for Autonomous Agents

## Project Identity
**Type:** Budgeting application
**Purpose:** Financial tracking and planning
**Architecture:** Monorepo with separate frontend/backend
**Languages:** Python (backend), TypeScript (frontend)

## Runtime Environment
- **Backend:** Python v3.12
- **Frontend:** Node.js v24.11.0 (LTS)
- **Package Managers:** pip (backend), npm (frontend)
- **Monorepo Structure:**
  - `/backend` - FastAPI server
  - `/frontend` - React Native mobile app
  - Separate `.env` files per workspace

## Tech Stack

### Backend (FastAPI)
**Framework:** FastAPI
**Database:** PostgreSQL v18.0
**ORM:** SQLAlchemy (async) with asyncpg driver
**Runtime:** Python v3.12

**Key Dependencies:**
- **Framework:** `fastapi`, `uvicorn[standard]`
- **Database:** `sqlalchemy[asyncio]`, `asyncpg`, `alembic`
- **Security:** `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`
- **Validation:** `pydantic` (built into FastAPI), `pydantic-settings`
- **CORS:** `fastapi.middleware.cors` (built-in)
- **Caching:** `redis`, `redis-py`
- **Data Processing:** `pandas`, `python-dateutil`
- **Background Tasks:** `celery`, `celery[redis]`
- **Testing:** `pytest`, `pytest-asyncio`, `httpx`, `pytest-cov`
- **API Docs:** Auto-generated OpenAPI/Swagger (built into FastAPI)

**Dev Dependencies:** `black`, `flake8`, `mypy`, `isort`, `pre-commit`

### Frontend (React Native)
**Framework:** React Native v0.81.5  
**Runtime:** Node v24.11.0, TypeScript v5.9.3

**Key Dependencies:**
- **Navigation:** `@react-navigation/native`, `@react-navigation/native-stack`, `react-native-screens`, `react-native-safe-area-context`
- **HTTP Client:** `axios`
- **State Management:** `zustand`, `@tanstack/react-query`
- **Forms:** `react-hook-form`
- **Validation:** `zod` or `yup` (client-side validation)
- **Charts:** `react-native-chart-kit`, `react-native-svg`
- **Utilities:** `date-fns`, `@react-native-async-storage/async-storage`
- **Testing:** `playwright`

### Infrastructure
**Containerization:** Docker + Docker Compose

**Services:**
1. **Backend API** - FastAPI server (async)
2. **Database** - PostgreSQL 18.0
3. **Redis** - Caching and Celery broker
4. **Celery Worker** - Background task processing
5. **Claude Code Agent** - Dedicated slim container for AI agent interaction with environment

## Critical Patterns for Agents

### Validation Schema Strategy
- **Backend:** Pydantic models (built into FastAPI)
- **Frontend:** Zod or Yup for client-side validation
- Define API contracts with Pydantic schemas in `/backend/app/schemas`
- Frontend can consume OpenAPI spec for type generation

### Type Safety
- **Backend:** Python 3.12 type hints with mypy static checking
- **Frontend:** TypeScript v5.9.3 strict mode
- SQLAlchemy async models generate typed ORM interfaces
- Share API contracts via auto-generated OpenAPI/Swagger spec

### Date Handling
- **Backend:** Use `datetime` (stdlib) and `python-dateutil` for parsing
- **Frontend:** Use `date-fns` for formatting and manipulation
- API communication: ISO 8601 strings (FastAPI auto-serializes datetime objects)

### Decimal Precision
- **Backend:** Use `decimal.Decimal` (stdlib) for all financial calculations
- **Frontend:** Use `decimal.js` for currency operations
- **Critical:** Never use float/double for currency on either side

### Environment Configuration
- Separate `.env` files: `.env.backend`, `.env.frontend`
- Never commit secrets
- Document required variables in `.env.example` files

### API Standards
- RESTful conventions with FastAPI path operations
- Auto-generated OpenAPI docs at `/docs` (Swagger UI)
- ReDoc documentation at `/redoc`
- JWT authentication via HTTP-only cookies
- Rate limiting via middleware (if needed)

### Development Workflow
- **Backend:** `pytest` with `pytest-asyncio` for async tests, `uvicorn --reload` for hot reload
- **Frontend:** `playwright` for E2E testing
- **Code Quality:**
  - Backend: `black` (formatting), `flake8` (linting), `isort` (imports), `mypy` (type checking)
  - Frontend: `eslint` + `prettier`
- **Background Tasks:** Celery workers with Redis broker

## Agent-Specific Notes

### When modifying backend:
1. Update SQLAlchemy models in `/backend/app/models/` for DB changes
2. Create migrations: `alembic revision --autogenerate -m "description"`
3. Apply migrations: `alembic upgrade head`
4. Update Pydantic schemas in `/backend/app/schemas/` for request/response validation
5. FastAPI auto-updates OpenAPI docs (no manual annotations needed for basic cases)
6. For background tasks, create Celery tasks in `/backend/app/tasks/`

### When modifying frontend:
1. Ensure React Native compatibility (no web-only APIs)
2. Update navigation types if routes change
3. Use Zustand for global state, React Query for server state
4. Test on both iOS/Android if UI changes

### Docker operations:
1. Backend/Frontend have separate Dockerfiles
2. Claude Code container shares network with services
3. Use volume mounts for hot reload in development
4. PostgreSQL data persists via named volume

### Common commands (likely):
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head

# Backend development
uvicorn app.main:app --reload  # Start FastAPI server
celery -A app.celery worker --loglevel=info  # Start Celery worker
pytest  # Run tests
pytest --cov=app tests/  # Run tests with coverage

# Backend code quality
black .  # Format code
isort .  # Sort imports
flake8  # Lint
mypy .  # Type check

# Frontend
cd frontend
npm install
npm run start
npm run android
npm run ios
```

## File Structure Assumptions
```
/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API route handlers
│   │   ├── tasks/           # Celery tasks
│   │   ├── database.py      # Database session management
│   │   └── celery.py        # Celery configuration
│   ├── alembic/             # Database migrations
│   │   └── versions/
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   ├── alembic.ini
│   └── pyproject.toml       # Optional: for tool configs
├── frontend/
│   ├── src/
│   ├── .env
│   └── package.json
├── docker-compose.yml
└── package.json             # Root npm scripts for frontend
```
