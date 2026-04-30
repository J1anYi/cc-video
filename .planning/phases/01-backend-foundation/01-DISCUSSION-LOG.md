# Phase 1: Backend Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-29
**Phase:** 01-backend-foundation
**Areas discussed:** Backend Framework, Database, Authentication, Session Management, Admin Role Enforcement, API Documentation

---

## Backend Framework

| Option | Description | Selected |
|--------|-------------|----------|
| FastAPI | Modern Python async framework with auto OpenAPI docs | ✓ |
| Express.js | Node.js framework, flexible but requires more setup | |
| Django | Full-featured Python framework, may be overkill for API-only | |
| Flask | Lightweight Python framework, requires more manual setup | |

**User's choice:** FastAPI (auto-selected - recommended)
**Notes:** Greenfield project with clear API boundaries; FastAPI provides strong typing, auto documentation, and async support out of the box.

---

## Database

| Option | Description | Selected |
|--------|-------------|----------|
| SQLite + SQLAlchemy | Zero-config dev, ORM abstraction, easy migration path | ✓ |
| PostgreSQL | Production-grade, requires separate setup | |
| MongoDB | NoSQL, less structured for relational data | |

**User's choice:** SQLite + SQLAlchemy (auto-selected - recommended)
**Notes:** Start simple for v1, SQLAlchemy ORM provides migration path to PostgreSQL if needed later.

---

## Authentication

| Option | Description | Selected |
|--------|-------------|----------|
| JWT + httpOnly cookies | Stateless, secure cookie storage, good for SPAs | ✓ |
| Session cookies | Traditional, requires server-side session store | |
| OAuth2 only | Third-party auth only, no local accounts | |

**User's choice:** JWT + httpOnly cookies (auto-selected - recommended)
**Notes:** Works well for separated frontend/backend; httpOnly prevents XSS; refresh tokens enable session persistence.

---

## Session Management

| Option | Description | Selected |
|--------|-------------|----------|
| Access + Refresh tokens | Short-lived access, long-lived refresh for persistence | ✓ |
| Long-lived JWT only | Simpler but less secure | |
| Session store | Server-side sessions, requires sticky sessions or shared store | |

**User's choice:** Access + Refresh tokens (auto-selected - recommended)
**Notes:** Balances security (short access token lifetime) with UX (refresh keeps user logged in across browser refresh).

---

## Admin Role Enforcement

| Option | Description | Selected |
|--------|-------------|----------|
| RBAC middleware | Role field on user, middleware checks before admin endpoints | ✓ |
| Hardcoded admin check | Simple if statement in each endpoint | |
| Permission system | Granular permissions per action | |

**User's choice:** RBAC middleware (auto-selected - recommended)
**Notes:** Clean separation of concerns, extensible if more roles needed later.

---

## API Documentation

| Option | Description | Selected |
|--------|-------------|----------|
| FastAPI auto OpenAPI/Swagger | Zero-config, interactive playground | ✓ |
| Manual OpenAPI spec | Full control but maintenance burden | |
| API Blueprint | Alternative format, less common | |

**User's choice:** FastAPI auto OpenAPI/Swagger (auto-selected - recommended)
**Notes:** Automatic documentation from type hints, interactive testing UI, can generate frontend client types.

---

## Claude's Discretion

- Specific library versions and minor implementation details
- Error response format standardization
- Logging configuration
- Environment variable naming conventions

## Deferred Ideas

None — discussion stayed within phase scope.
