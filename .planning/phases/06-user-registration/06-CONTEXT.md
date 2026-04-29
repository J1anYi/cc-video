# Phase 6 Context: User Registration

## Context Gathering Date: 2026-04-29

## Phase Goal

Allow new users to create accounts without admin intervention.

**Requirements:** ACC-01, ACC-02, ACC-03

## Decisions

### Registration Flow

**Decision:** Auto-login after successful registration (redirect to catalog)

**Rationale:** Best UX - users can immediately start using the app. Alternative is redirect to login page which requires users to re-enter credentials.

**Implementation:**
- Registration returns access token (same response as login)
- Frontend stores token and navigates to /movies
- Same token cookie flow as login

### Password Validation

**Decision:** Minimum 8 characters, no additional complexity requirements

**Rationale:** 
- v1.1 is MVP - simple but reasonable security
- Overly complex rules frustrate users
- 8 characters provides adequate baseline
- Future: could add password strength meter, complexity rules

**Implementation:**
- Frontend: HTML5 minlength="8" validation
- Backend: Pydantic field validator for length
- No special character requirements

### Username Handling

**Decision:** Use existing email field as username

**Rationale:**
- Backend already uses email as unique identifier
- No need to add separate username field
- Login already accepts email (OAuth2PasswordRequestForm.username)
- Simpler data model

**Implementation:**
- Registration form labels "Email" but sends as username
- Backend validates email format with EmailStr
- Unique constraint already exists on email field

### Error Messages

**Decision:** Specific error for duplicate email, generic for other failures

**Rationale:**
- Users need to know if email is already taken (so they can login instead)
- Other errors should be generic to avoid information leakage
- Clear UX: "Email already registered" → user can go to login

**Implementation:**
- Backend: Check for unique constraint violation
- Frontend: Display error message with link to login

### Rate Limiting

**Decision:** Deferred to future release

**Rationale:**
- v1.1 is internal/demo phase
- No production exposure yet
- Can add in v1.2 when deploying publicly
- Keeps implementation simple for MVP

### UI Placement

**Decision:** Add "Register" link on login page, separate registration page at /register

**Rationale:**
- Standard pattern users expect
- Login page already exists with good styling
- Registration page mirrors login layout
- Clear navigation between login/register

**Implementation:**
- New route: /register
- Link on login page: "Don't have an account? Register"
- Link on register page: "Already have an account? Login"

## Code Context

### Reusable Assets

1. **Backend Auth Service** (`backend/app/services/auth.py`)
   - `get_password_hash()` - for hashing passwords
   - `create_access_token()` - for generating JWT
   - `create_refresh_token()` - for refresh tokens

2. **Backend User Service** (`backend/app/services/user.py`)
   - `create()` method already exists!
   - Accepts email, password, role
   - Hashes password automatically
   - Default role is USER

3. **Frontend Auth Context** (`frontend/src/auth/AuthContext.tsx`)
   - `login()` function stores token
   - Can create similar `register()` function
   - Token storage logic reusable

### Gaps to Fill

1. **Backend:**
   - Add public `/auth/register` endpoint
   - No changes needed to user service (create() already exists)
   - Schema: UserCreate already exists with email + password

2. **Frontend:**
   - Create Register.tsx component (copy Login.tsx structure)
   - Add register() to AuthContext
   - Add API call to /auth/register
   - Add /register route to router

### File Changes Expected

**Backend:**
- `backend/app/routes/auth.py` - Add register endpoint

**Frontend:**
- `frontend/src/routes/Register.tsx` - New file
- `frontend/src/auth/AuthContext.tsx` - Add register function
- `frontend/src/api/auth.ts` - Add register API call
- `frontend/src/App.tsx` - Add /register route

## Success Criteria Mapping

| Criterion | Implementation |
|-----------|----------------|
| Public registration page accessible | New /register route, no auth required |
| Form validates username/password | Frontend HTML5 + backend Pydantic |
| Username uniqueness validated | Backend checks email unique constraint |
| Password meets requirements | 8 character minimum validation |
| Redirect after success | Auto-login, redirect to /movies |
| Default user role | user_service.create() defaults to USER |

## Notes

- User service already has everything we need - minimal backend work
- Frontend work is primarily creating Register component
- Can leverage existing patterns from Login.tsx
- Consider this phase "light" - most infrastructure exists
