# Phase 1: Backend Foundation - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase establishes the backend API foundation with database persistence, authentication, session behavior, and administrator role enforcement. The frontend is intentionally separate — this phase delivers only the backend API and database schema.

**In scope:**
- Backend API framework setup
- Database schema for users, roles, movies, video file metadata
- Authentication endpoints (login, logout, current user)
- Session management that persists across browser refresh
- Admin role enforcement for protected endpoints
- API documentation for frontend consumption

**Out of scope:**
- Frontend implementation (Phase 3, 4)
- Video file upload handling (Phase 2)
- Movie catalog browsing (Phase 3)
- Video playback serving (Phase 3)

</domain>

<decisions>
## Implementation Decisions

### Backend Framework
- **D-01:** Use **FastAPI** as the backend framework
  - Rationale: Modern Python async framework, automatic OpenAPI documentation, strong typing with Pydantic, excellent for REST APIs. Well-suited for a greenfield project with clear API boundaries.

### Database
- **D-02:** Use **SQLite** for development with **SQLAlchemy** ORM
  - Rationale: Zero-config for development, easy to migrate to PostgreSQL later if needed. SQLAlchemy provides database-agnostic ORM and migration support via Alembic.

### Authentication
- **D-03:** Use **JWT tokens** with httpOnly cookies for authentication
  - Rationale: Stateless auth works well for separated frontend/backend architecture. httpOnly cookies prevent XSS token theft. Refresh tokens enable session persistence across browser refresh.

### Session Management
- **D-04:** Implement **access token + refresh token** pattern
  - Rationale: Short-lived access tokens (15-30 min) for security, long-lived refresh tokens for session persistence. Refresh tokens stored in httpOnly cookies, access tokens in memory or httpOnly cookies.

### Admin Role Enforcement
- **D-05:** Implement **role-based access control (RBAC)** middleware
  - Rationale: Simple role field on user model, middleware checks role before allowing admin endpoints. Clean separation of concerns.

### API Documentation
- **D-06:** Use **FastAPI's auto-generated OpenAPI/Swagger UI**
  - Rationale: Zero-config API documentation, interactive playground for testing, OpenAPI spec can be used to generate frontend client types.

### Project Structure
- **D-07:** Use **src/ layout** with clear module separation
  - Structure: `backend/` directory with `app/`, `models/`, `routes/`, `services/`, `schemas/`, `middleware/`

### Claude's Discretion
- Specific library versions and minor implementation details
- Error response format standardization
- Logging configuration
- Environment variable naming conventions

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Documentation
- `.planning/PROJECT.md` — Project vision, constraints, key decisions
- `.planning/REQUIREMENTS.md` — AUTH-01, AUTH-02, AUTH-03, AUTH-04, API-01, API-02 requirements
- `.planning/ROADMAP.md` — Phase 1 goal and success criteria

### External References (to be consulted)
- FastAPI documentation — https://fastapi.tiangolo.com/
- SQLAlchemy documentation — https://docs.sqlalchemy.org/
- OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

</canonical_refs>

<code_context>
## Existing Code Insights

### Current State
- Greenfield project — no existing backend code
- Repository contains only planning documents and empty README

### Integration Points
- Backend will be created under `backend/` directory
- API will be exposed at configurable port (default 8000)
- Database file will be `backend/data/cc_video.db` (SQLite)

</code_context>

<specifics>
## Specific Ideas

- Keep route contracts clear because the frontend is intentionally separate
- This phase should choose the concrete backend framework, database library, and auth mechanism
- Success criteria includes: backend exposes documented auth and current-user APIs for the frontend

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-backend-foundation*
*Context gathered: 2026-04-29*
