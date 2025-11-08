# Project Context for Autonomous Agents

## Project Identity
**Type:** Budgeting application  
**Purpose:** Financial tracking and planning  
**Architecture:** Monorepo with separate frontend/backend  
**Language:** TypeScript throughout

## Runtime Environment
- **Node.js:** v24.11.0 (LTS)
- **Package Manager:** (specify: npm/yarn/pnpm)
- **Monorepo Structure:** 
  - `/backend` - Fastify API server
  - `/frontend` - React Native mobile app
  - Separate `.env` files per workspace

## Tech Stack

### Backend (Fastify API)
**Framework:** Fastify v5.6.x  
**Database:** PostgreSQL v18.0  
**ORM:** Prisma  
**Runtime:** Node v24.11.0, TypeScript v5.9.3

**Key Dependencies:**
- **Security:** `@fastify/cors`, `@fastify/helmet`, `@fastify/rate-limit`, `@fastify/jwt`, `@fastify/cookie`
- **File Upload:** `@fastify/multipart`
- **Logging:** `pino`, `pino-pretty`
- **Data Processing:** `csv-parse`, `csv-stringify`, `date-fns`, `decimal.js`
- **Auth:** `bcrypt`, `@types/bcrypt`
- **Caching:** `ioredis`, `@types/ioredis`
- **API Docs:** `@fastify/swagger`, `@fastify/swagger-ui`
- **Validation:** `@sinclair/typebox`

**Dev Dependencies:** `typescript`, `@types/node`, `tsx`, `eslint`, `prettier`, `vitest`, `@vitest/ui`, `nodemon`

### Frontend (React Native)
**Framework:** React Native v0.81.5  
**Runtime:** Node v24.11.0, TypeScript v5.9.3

**Key Dependencies:**
- **Navigation:** `@react-navigation/native`, `@react-navigation/native-stack`, `react-native-screens`, `react-native-safe-area-context`
- **HTTP Client:** `axios`
- **State Management:** `zustand`, `@tanstack/react-query`
- **Forms:** `react-hook-form`
- **Validation:** `@sinclair/typebox` (shared with backend)
- **Charts:** `react-native-chart-kit`, `react-native-svg`
- **Utilities:** `date-fns`, `@react-native-async-storage/async-storage`
- **Testing:** `playwright`

### Infrastructure
**Containerization:** Docker + Docker Compose

**Services:**
1. **Backend API** - Fastify server
2. **Database** - PostgreSQL 18.0
3. **Redis** - Caching layer (ioredis)
4. **Claude Code Agent** - Dedicated slim container for AI agent interaction with environment

## Critical Patterns for Agents

### Shared Validation Schema
- Both frontend/backend use `@sinclair/typebox`
- Define schemas once, import across workspaces
- Location: `/shared/schemas` or `/packages/shared`

### Type Safety
- TypeScript v5.9.3 strict mode expected
- Prisma generates backend types
- Share API types between frontend/backend

### Date Handling
- Use `date-fns` consistently (installed on both sides)
- Avoid native Date() inconsistencies

### Decimal Precision
- Use `decimal.js` for financial calculations
- Never use floating-point for currency

### Environment Configuration
- Separate `.env` files: `.env.backend`, `.env.frontend`
- Never commit secrets
- Document required variables in `.env.example` files

### API Standards
- RESTful conventions
- Swagger/OpenAPI documentation at `/docs`
- JWT authentication via cookies
- Rate limiting enabled

### Development Workflow
- `vitest` for backend testing
- `playwright` for frontend E2E testing
- `eslint` + `prettier` for code quality
- `nodemon` for backend hot reload

## Agent-Specific Notes

### When modifying backend:
1. Update Prisma schema if DB changes needed
2. Run `prisma generate` after schema changes
3. Create migrations with `prisma migrate dev`
4. Update Swagger annotations for API docs
5. Validate with TypeBox schemas

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
# Root level
npm install
npm run dev

# Backend
cd backend
npm run dev
npm run test
npx prisma studio

# Frontend  
cd frontend
npm run start
npm run android
npm run ios
```

## File Structure Assumptions
```
/
├── backend/
│   ├── src/
│   ├── prisma/
│   ├── .env
│   └── package.json
├── frontend/
│   ├── src/
│   ├── .env
│   └── package.json
├── shared/ (or packages/shared)
│   └── schemas/
├── docker-compose.yml
└── package.json
```
