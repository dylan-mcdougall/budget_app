# 2025-11-22 - Database Schema Setup

**Tags:** #database #backend #sqlalchemy #uuidv7
**Status:** Complete

## Summary
Created comprehensive SQLAlchemy ORM models for budgeting application core entities. Implemented UUIDv7 primary keys for temporal ordering, Decimal monetary fields for precision, and async-first design patterns. All 6 domain models established with proper relationships, enums, and validation.

## Context
- **Need:** Foundation for PostgreSQL database schema with type-safe ORM access
- **Constraints:** Must support async operations (asyncpg), prevent floating-point currency errors, maintain backward compatibility with migrations
- **Related:** Base project setup (commit fa07d9d)

## Changes

**Files Created:**
- `backend/app/models/base.py` - Base classes with UUIDv7 and timestamp mixins
- `backend/app/models/user.py` - User entity with auth fields
- `backend/app/models/account.py` - Financial accounts with 7 types
- `backend/app/models/category.py` - Transaction categories with hierarchy
- `backend/app/models/transaction.py` - Financial transactions (income/expense/transfer)
- `backend/app/models/budget.py` - Spending limits with 5 period types
- `backend/app/models/__init__.py` - Model exports

**Files Updated:**
- `/workspace/requirements.txt` - Added backend dependencies

## Technical Decisions

### UUIDv7 Over UUID4
- Time-ordered UUIDs improve database index performance
- Clustered index locality benefits PostgreSQL sequential writes
- uuid6 library provides native Python implementation
- Migration-friendly (no schema change required)

### Decimal for Currency
- SQLAlchemy `Numeric` type maps to PostgreSQL `NUMERIC`
- Prevents IEEE 754 floating-point errors (precision to 2 decimals via DB constraint)
- Matches CLAUDE.md requirement for financial calculations

### Model Structure
```
Base (DeclarativeBase)
├── TimestampMixin (created_at, updated_at with server defaults)
└── UUIDMixin (id: UUID primary key with uuid7 default)
    ├── User (auth: email, password_hash, full_name)
    ├── Account (accounts: type enum, balance, currency)
    ├── TransactionCategory (hierarchy via parent_category_id)
    ├── Transaction (multi-type with linked_transfer support)
    └── Budget (period enum, category limits)
```

### Async-First Design
- All models use `mapped_column()` with SQLAlchemy 2.0 style
- No synchronous session assumptions
- Compatible with async context in FastAPI

### Enums Used
- `AccountType`: checking, savings, credit_card, cash, investment, loan, other
- `TransactionType`: income, expense, transfer
- `CategoryType`: income, expense
- `BudgetPeriod`: daily, weekly, monthly, quarterly, yearly

## Dependencies Added
```
sqlalchemy[asyncio]==2.0.23  # Async ORM
asyncpg==0.29.0             # PostgreSQL async driver
alembic==1.13.0             # Migration tool
uuid6==2024.1.12            # UUIDv7 support
pydantic==2.5.0             # Validation (FastAPI bundled)
```

## Key Model Features

**User**: email (unique), password_hash, full_name, created_at, updated_at

**Account**:
- user_id (FK), account_type (enum), name, balance (Decimal), currency
- Indexes: (user_id, created_at), account_type

**TransactionCategory**:
- user_id (FK), name, category_type (enum), parent_category_id (self-FK)
- Supports subcategories (e.g., "Groceries" under "Food")
- Index: (user_id, category_type)

**Transaction**:
- user_id (FK), from_account_id (FK), to_account_id (FK), transaction_type (enum), amount (Decimal), description
- linked_transaction_id (self-FK) for transfer pairs
- Index: (user_id, created_at)

**Budget**:
- user_id (FK), category_id (FK), limit (Decimal), period (enum), fiscal_year
- Track spending limits per category/period
- Index: (user_id, period)

## Issues Resolved
None - greenfield implementation

## Attempted
- UUIDv7 + SQLAlchemy type stubs: Native support via uuid6 library works seamlessly

## Next Steps
- [ ] Create Alembic migration configuration (`alembic init`)
- [ ] Generate initial migration (`alembic revision --autogenerate`)
- [ ] Implement database.py (async session factory, engine config)
- [ ] Create Pydantic schemas in `app/schemas/` for API validation
- [ ] Write model tests in `tests/models/`
- [ ] Update CLAUDE.md with model examples if needed

## For AI Agents
- All monetary fields use `Numeric(precision=19, scale=2)` - enforce at schema validation too
- Foreign keys use `ondelete="CASCADE"` except user_id relationships (use "SET NULL" if soft deletes added)
- Model imports via `__init__.py` - keep exports current
- Timestamp fields use PostgreSQL server defaults - don't set in Python
- Account transfers: create two linked transactions (one from_account, one to_account, same linked_transaction_id)

## Environment
- Python: 3.12+ (async support required)
- Branch: main
- Commit: 36286cb (merge PR #2)

---
**Agent:** Claude Code | **Model:** claude-haiku-4-5-20251001
