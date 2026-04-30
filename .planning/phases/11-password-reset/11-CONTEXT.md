# Phase 11: Password Reset - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning
**Source:** Auto-generated from PROJECT.md and REQUIREMENTS.md

<domain>
## Phase Boundary

This phase delivers email-based password reset functionality. Users can request a password reset from the login page, receive an email with a secure reset link, and set a new password.

**In scope:**
- Password reset request endpoint
- Email with secure reset token
- Reset token validation and expiration
- New password setting endpoint
- Frontend reset request and reset forms

**Out of scope:**
- Email infrastructure setup (assumes SMTP or external service available)
- Two-factor authentication
- Account deletion

</domain>

<decisions>
## Implementation Decisions

### Backend
- Generate secure random tokens for password reset (secrets.token_urlsafe)
- Store reset tokens in database with expiration (1 hour default)
- Send emails via FastAPI background tasks
- Invalidate tokens after use

### Frontend
- Add "Forgot Password" link on login page
- Create password reset request page
- Create password reset form page (accessed via email link)

### Security
- Token expiration: 1 hour
- Token invalidation after successful password reset
- Rate limiting on reset request endpoint (prevent abuse)

### Claude's Discretion
- Email service implementation details
- Token storage schema (new table vs User model field)
- Frontend routing structure

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Authentication
- `backend/app/routes/auth.py` — Current login/logout implementation
- `backend/app/models/user.py` — User model structure
- `backend/app/services/auth.py` — Authentication service
- `frontend/src/routes/Login.tsx` — Current login page

</canonical_refs>

<specifics>
## Specific Ideas

- Reset flow: User clicks "Forgot Password" → enters email → receives email with link → clicks link → enters new password → redirected to login
- Token format: URL-safe random string, stored hashed in database
- Email content: Link with token, expiration notice

</specifics>

<deferred>
## Deferred Ideas

None — scope is clear from requirements

</deferred>

---

*Phase: 11-password-reset*
*Context gathered: 2026-04-29*
