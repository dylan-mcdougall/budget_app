# Claude Code Project Context

## Project Overview

This is a **budgeting application** for financial tracking and planning, built as a monorepo with separate frontend and backend workspaces.

**Architecture:**
- **Backend:** FastAPI server with PostgreSQL database (Python 3.12)
- **Frontend:** React Native mobile application (TypeScript)
- **Runtime:** Python 3.12 (backend), Node.js v24.11.0 LTS (frontend)
- **Infrastructure:** Docker Compose with PostgreSQL, Redis, Celery, and application services

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js v24.11.0 (for frontend)
- Docker and Docker Compose
- PostgreSQL 18.0 (via Docker)
- Redis (via Docker)

### Initial Setup
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure environment variables
alembic upgrade head  # Run database migrations

# Frontend setup
cd ../frontend
npm install
cp .env.example .env  # Configure environment variables
```

### Running the Application
```bash
# Backend (from backend directory)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload  # FastAPI server
celery -A app.celery worker --loglevel=info  # Celery worker (separate terminal)

# Frontend
cd frontend
npm run start
npm run android  # For Android
npm run ios      # For iOS
```

## Project Structure

```
/
├── backend/           # FastAPI server
│   ├── app/          # Application code
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── routers/  # API route handlers
│   │   ├── tasks/    # Celery tasks
│   │   └── main.py   # FastAPI app entry point
│   ├── alembic/      # Database migrations
│   ├── tests/        # Backend tests
│   ├── .env          # Backend environment variables
│   └── requirements.txt
├── frontend/         # React Native mobile app
│   ├── src/          # Source code
│   ├── .env          # Frontend environment variables
│   └── package.json
├── docker-compose.yml
└── package.json      # Root package.json (frontend scripts)
```

## Technology Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL 18.0
- **ORM:** SQLAlchemy (async) with asyncpg driver
- **Migrations:** Alembic
- **Validation:** Pydantic (built into FastAPI)
- **Authentication:** JWT with HTTP-only cookies (python-jose, passlib)
- **Security:** CORS middleware (built-in), security headers
- **Testing:** pytest, pytest-asyncio, httpx
- **Caching:** Redis (redis-py)
- **Background Tasks:** Celery with Redis broker
- **Data Processing:** pandas

### Frontend
- **Framework:** React Native v0.81.5
- **Navigation:** @react-navigation/native
- **State Management:** zustand (global), @tanstack/react-query (server state)
- **HTTP Client:** axios
- **Forms:** react-hook-form
- **Charts:** react-native-chart-kit, react-native-svg
- **Testing:** playwright
- **Storage:** @react-native-async-storage/async-storage

## Critical Development Patterns

### 1. Financial Calculations
**ALWAYS use appropriate decimal libraries for currency calculations**

**Backend (Python):**
```python
from decimal import Decimal

# ✅ CORRECT
total = Decimal(str(price)) * Decimal(str(quantity))

# ❌ WRONG - floating point errors!
total = price * quantity
```

**Frontend (TypeScript):**
```typescript
import Decimal from 'decimal.js';

// ✅ CORRECT
const total = new Decimal(price).times(quantity);

// ❌ WRONG - floating point errors!
const total = price * quantity;
```

### 2. Date Handling
**Use appropriate date libraries for each platform**

**Backend (Python):**
```python
from datetime import datetime, timedelta
from dateutil.parser import parse

# Use ISO 8601 for API responses (FastAPI handles serialization automatically)
date = datetime.now()
```

**Frontend (TypeScript):**
```typescript
import { format, parseISO, addDays } from 'date-fns';

// Consistent formatting and parsing
const formatted = format(new Date(), 'yyyy-MM-dd');
```

### 3. Validation Schemas
**Use Pydantic for backend, Zod/Yup for frontend**
- **Backend:** Define Pydantic models in `/backend/app/schemas`
- **Frontend:** Mirror validation logic with Zod or Yup
- Share API contracts via auto-generated OpenAPI spec
- FastAPI auto-generates documentation at `/docs`

### 4. Type Safety
- **Backend:** Python 3.12 type hints with mypy static type checking
- **Frontend:** TypeScript v5.9.3 strict mode
- SQLAlchemy models provide typed ORM interfaces
- Share API types via OpenAPI/Swagger spec
- **Python:** Avoid `Any` - use `object` or proper type hints
- **TypeScript:** Never use `any` - prefer `unknown` if type is truly unknown

### 5. Environment Variables
- Separate `.env` files: backend and frontend
- Document all required variables in `.env.example`
- Never commit secrets or `.env` files
- **Backend:** Use `pydantic-settings` for environment configuration
- **Frontend:** Access via `process.env.VARIABLE_NAME`

### 6. API Conventions
- RESTful endpoints using FastAPI path operations
- JWT authentication via HTTP-only cookies
- Rate limiting via middleware (optional)
- Auto-generated OpenAPI documentation at `/docs` (Swagger UI)
- ReDoc documentation at `/redoc`
- Pydantic models automatically generate request/response schemas

## Common Development Tasks

### Backend Modifications

1. **Database Changes:**
   ```bash
   # Edit SQLAlchemy models in app/models/
   alembic revision --autogenerate -m "description"
   alembic upgrade head
   ```

2. **Adding API Endpoints:**
   - Create route handler in `app/routers/`
   - Define Pydantic schemas in `app/schemas/`
   - FastAPI auto-generates OpenAPI docs
   - Write tests in `tests/`

3. **Running Tests:**
   ```bash
   cd backend
   pytest
   pytest --cov=app tests/  # With coverage
   ```

4. **Database Management:**
   - Use PostgreSQL CLI or GUI tools (pgAdmin, DBeaver)
   - SQLAlchemy session management in `app/database.py`

### Frontend Modifications

1. **Adding Screens:**
   - Create component in `src/screens/`
   - Update navigation types
   - Ensure React Native compatibility (no web-only APIs)

2. **State Management:**
   - Use **Zustand** for global app state
   - Use **React Query** for server state/caching
   - Keep state as close to where it's used as possible

3. **Testing:**
   ```bash
   cd frontend
   npm run test  # Playwright E2E tests
   ```

### Docker Operations

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Rebuild after dependency changes
docker-compose up --build
```

## Code Quality Standards

### Linting and Formatting

**Backend (Python):**
```bash
cd backend
black .       # Format code
isort .       # Sort imports
flake8        # Lint
mypy .        # Type check
```

**Frontend (TypeScript):**
```bash
cd frontend
npm run lint   # ESLint
npm run format # Prettier
```

### Testing Requirements
- Write unit tests for business logic
- **Backend:** pytest for API and service tests, pytest-asyncio for async code
- **Frontend:** playwright for E2E user flows
- Aim for >80% coverage on critical paths
- Use httpx for testing FastAPI endpoints

## Security Considerations

1. **Authentication:** JWT tokens stored in HTTP-only cookies
2. **Rate Limiting:** Optional middleware (slowapi for FastAPI)
3. **CORS:** Configured for allowed origins via FastAPI middleware
4. **Security Headers:** Configured via middleware
5. **Input Validation:** All inputs validated with Pydantic
6. **SQL Injection:** Prevented by SQLAlchemy ORM (parameterized queries)
7. **Password Hashing:** bcrypt via passlib
8. **Secrets:** Never commit `.env` files

## Common Pitfalls to Avoid

1. **Don't** use floating-point math for currency (use Decimal in Python, decimal.js in TypeScript)
2. **Don't** use synchronous database operations (use async SQLAlchemy)
3. **Don't** use web-only APIs in React Native code
4. **Don't** forget to run `alembic upgrade head` after pulling new migrations
5. **Don't** commit database migrations without testing them
6. **Don't** bypass Pydantic validation schemas
7. **Don't** store sensitive data in frontend state
8. **Don't** use mutable default arguments in Python functions

## Debugging Tips

### Backend
- Check logs: `docker-compose logs -f backend`
- FastAPI logs via uvicorn (structured logging)
- SQLAlchemy debugging: Set `echo=True` in engine configuration
- Use PostgreSQL client tools for database inspection
- Celery tasks: `celery -A app.celery inspect active`

### Frontend
- React Native debugger for mobile
- Network requests: inspect axios calls
- State: Use Zustand devtools
- React Query devtools for server state

## File Naming Conventions

**Backend (Python):**
- **Modules/Files:** snake_case (e.g., `user_profile.py`)
- **Classes:** PascalCase (e.g., `UserProfile`)
- **Functions/Variables:** snake_case (e.g., `format_currency`)
- **Tests:** Same name as file with `test_` prefix (e.g., `test_user_profile.py`)

**Frontend (TypeScript):**
- **Components:** PascalCase (e.g., `UserProfile.tsx`)
- **Utilities:** camelCase (e.g., `formatCurrency.ts`)
- **Tests:** Same name as file with `.test.ts` or `.spec.ts`

## When Working on This Project

1. **Read the code first** - Understand existing patterns before adding new code
2. **Follow established conventions** - Match the style of surrounding code
3. **Test your changes** - Run relevant tests before committing
4. **Update models** - Create Alembic migrations if SQLAlchemy models change
5. **Document APIs** - FastAPI auto-generates docs, but add descriptions to endpoints
6. **Consider both platforms** - Frontend changes should work on iOS and Android
7. **Use async/await** - Backend uses async SQLAlchemy, always use async patterns
8. **Type hints** - Always add Python type hints for better IDE support and mypy checking

## Getting Help

- Check `GETTING_STARTED.md` for detailed technical specifications
- Review existing code for examples of patterns
- Check Swagger docs at `/docs` for API reference
- Use TypeScript's type system to guide implementation

## Key Reminders for Claude

- This is a **financial application** - precision and security are critical
- **Backend:** Always use `decimal.Decimal` for money calculations
- **Frontend:** Always use `decimal.js` for money calculations
- Backend uses **async SQLAlchemy** - update models and run Alembic migrations for DB changes
- Frontend is **React Native** - not React for web, no DOM APIs
- **Type safety:** Python type hints + mypy for backend, TypeScript strict mode for frontend
- **FastAPI** auto-generates OpenAPI docs - leverage Pydantic for validation
- **Async patterns:** Use async/await throughout the Python backend
- **Test critical paths** - especially financial calculations and auth flows
- **Celery** for background tasks - don't block API responses with long-running operations
