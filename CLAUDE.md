# Claude Code Project Context

## Project Overview

This is a **budgeting application** for financial tracking and planning, built as a TypeScript monorepo with separate frontend and backend workspaces.

**Architecture:**
- **Backend:** Fastify API server with PostgreSQL database
- **Frontend:** React Native mobile application
- **Runtime:** Node.js v24.11.0 LTS
- **Infrastructure:** Docker Compose with PostgreSQL, Redis, and application services

## Development Setup

### Prerequisites
- Node.js v24.11.0
- Docker and Docker Compose
- PostgreSQL 18.0 (via Docker)
- Redis (via Docker)

### Initial Setup
```bash
# Install dependencies
npm install

# Backend setup
cd backend
npm install
cp .env.example .env  # Configure environment variables
npx prisma generate
npx prisma migrate dev

# Frontend setup
cd ../frontend
npm install
cp .env.example .env  # Configure environment variables
```

### Running the Application
```bash
# Development mode (from root)
npm run dev

# Backend only
cd backend
npm run dev

# Frontend only
cd frontend
npm run start
npm run android  # For Android
npm run ios      # For iOS
```

## Project Structure

```
/
├── backend/           # Fastify API server
│   ├── src/          # Source code
│   ├── prisma/       # Database schema and migrations
│   ├── .env          # Backend environment variables
│   └── package.json
├── frontend/         # React Native mobile app
│   ├── src/          # Source code
│   ├── .env          # Frontend environment variables
│   └── package.json
├── shared/           # Shared code and schemas
│   └── schemas/      # TypeBox validation schemas
├── docker-compose.yml
└── package.json      # Root package.json
```

## Technology Stack

### Backend
- **Framework:** Fastify v5.6.x
- **Database:** PostgreSQL 18.0
- **ORM:** Prisma
- **Validation:** @sinclair/typebox
- **Authentication:** JWT with cookies (@fastify/jwt, @fastify/cookie)
- **Security:** @fastify/cors, @fastify/helmet, @fastify/rate-limit
- **Logging:** pino, pino-pretty
- **Testing:** vitest, @vitest/ui
- **Caching:** ioredis

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
**ALWAYS use `decimal.js` for currency calculations**
```typescript
import Decimal from 'decimal.js';

// ✅ CORRECT
const total = new Decimal(price).times(quantity);

// ❌ WRONG - floating point errors!
const total = price * quantity;
```

### 2. Date Handling
**Use `date-fns` consistently across frontend and backend**
```typescript
import { format, parseISO, addDays } from 'date-fns';

// Avoid native Date() inconsistencies
```

### 3. Validation Schemas
**Share validation schemas between frontend and backend using TypeBox**
- Location: `/shared/schemas`
- Define once, import in both workspaces
- Ensures consistent validation rules

### 4. Type Safety
- TypeScript v5.9.3 strict mode
- Prisma generates database types automatically
- Share API types between frontend and backend
- Never use `any` - prefer `unknown` if type is truly unknown

### 5. Environment Variables
- Separate `.env` files: backend and frontend
- Document all required variables in `.env.example`
- Never commit secrets or `.env` files
- Access via `process.env.VARIABLE_NAME`

### 6. API Conventions
- RESTful endpoints
- JWT authentication via HTTP-only cookies
- Rate limiting enabled
- Swagger/OpenAPI documentation at `/docs`
- All endpoints documented with Swagger annotations

## Common Development Tasks

### Backend Modifications

1. **Database Changes:**
   ```bash
   # Edit prisma/schema.prisma
   npx prisma generate        # Regenerate types
   npx prisma migrate dev     # Create migration
   ```

2. **Adding API Endpoints:**
   - Create route handler in `src/routes/`
   - Add TypeBox validation schema
   - Update Swagger annotations
   - Write tests in `src/__tests__/`

3. **Running Tests:**
   ```bash
   cd backend
   npm run test
   ```

4. **Database Management:**
   ```bash
   npx prisma studio  # Visual database browser
   ```

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
```bash
# Run ESLint
npm run lint

# Run Prettier
npm run format

# Both are configured in .eslintrc and .prettierrc
```

### Testing Requirements
- Write unit tests for business logic
- Backend: vitest for API and service tests
- Frontend: playwright for E2E user flows
- Aim for >80% coverage on critical paths

## Security Considerations

1. **Authentication:** JWT tokens stored in HTTP-only cookies
2. **Rate Limiting:** Enabled on all API endpoints
3. **CORS:** Configured for allowed origins only
4. **Helmet:** Security headers enabled
5. **Input Validation:** All inputs validated with TypeBox
6. **SQL Injection:** Prevented by Prisma ORM
7. **Secrets:** Never commit `.env` files

## Common Pitfalls to Avoid

1. **Don't** use floating-point math for currency (use decimal.js)
2. **Don't** mutate Prisma results directly (they're frozen)
3. **Don't** use web-only APIs in React Native code
4. **Don't** forget to run `prisma generate` after schema changes
5. **Don't** commit database migrations without testing them
6. **Don't** bypass validation schemas
7. **Don't** store sensitive data in frontend state

## Debugging Tips

### Backend
- Check logs: `docker-compose logs -f backend`
- Use `pino-pretty` for readable logs
- Prisma debugging: Set `DEBUG=prisma:*`
- Use `npx prisma studio` for database inspection

### Frontend
- React Native debugger for mobile
- Network requests: inspect axios calls
- State: Use Zustand devtools
- React Query devtools for server state

## File Naming Conventions

- **Components:** PascalCase (e.g., `UserProfile.tsx`)
- **Utilities:** camelCase (e.g., `formatCurrency.ts`)
- **Routes:** kebab-case (e.g., `user-profile.ts`)
- **Tests:** Same name as file with `.test.ts` or `.spec.ts`

## When Working on This Project

1. **Read the code first** - Understand existing patterns before adding new code
2. **Follow established conventions** - Match the style of surrounding code
3. **Test your changes** - Run relevant tests before committing
4. **Update types** - Regenerate Prisma types if schema changes
5. **Document APIs** - Update Swagger annotations for new endpoints
6. **Consider both platforms** - Frontend changes should work on iOS and Android
7. **Use shared schemas** - Leverage TypeBox schemas for validation consistency

## Getting Help

- Check `GETTING_STARTED.md` for detailed technical specifications
- Review existing code for examples of patterns
- Check Swagger docs at `/docs` for API reference
- Use TypeScript's type system to guide implementation

## Key Reminders for Claude

- This is a **financial application** - precision and security are critical
- Always use **decimal.js** for money calculations
- Share validation logic between frontend and backend via **TypeBox schemas**
- Backend uses **Prisma ORM** - update schema and run migrations for DB changes
- Frontend is **React Native** - not React for web, no DOM APIs
- **TypeScript strict mode** - maintain type safety throughout
- **Test critical paths** - especially financial calculations and auth flows
