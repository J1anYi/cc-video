# Security Documentation

This document outlines the security measures implemented in CC Video.

## SEC-01: HTTPS Enforcement

### Implementation
- `HTTPSRedirectMiddleware` redirects HTTP to HTTPS in production
- HSTS header (`Strict-Transport-Security`) enforces HTTPS for 1 year
- Works with reverse proxy `X-Forwarded-Proto` header

### Configuration
- Automatic in production (`DEBUG=False`)
- Disabled in development for convenience

## SEC-02: Content Security Policy (CSP)

### Headers Implemented
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none';
```

### Additional Security Headers
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-XSS-Protection: 1; mode=block` - XSS filter (legacy)
- `Referrer-Policy: strict-origin-when-cross-origin` - Controls referrer info
- `Permissions-Policy: geolocation=(), microphone=(), camera=()` - Disables sensitive features

## SEC-03: SQL Injection Prevention

### Measures
1. **ORM Usage**: All database queries use SQLAlchemy ORM
2. **Parameterized Queries**: No raw SQL with string concatenation
3. **Input Validation**: Pydantic schemas validate all inputs
4. **Type Safety**: Type hints prevent type confusion

### Safe Patterns
```python
# SAFE: ORM query
result = await db.execute(select(User).where(User.email == email))

# SAFE: Parameterized query
result = await db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})

# UNSAFE: Never do this!
# result = await db.execute(text(f"SELECT * FROM users WHERE id = {user_id}"))
```

## SEC-04: XSS Prevention

### Measures
1. **Output Encoding**: `sanitize_html()` function escapes HTML entities
2. **CSP Headers**: Restricts script sources
3. **Input Validation**: Content length limits and type checking
4. **React**: Auto-escapes JSX content by default

### Sanitization Function
```python
from app.middleware.security import sanitize_html

# Escape user input before storage or display
safe_text = sanitize_html(user_input)
```

### Frontend Best Practices
- Never use `dangerouslySetInnerHTML` with user content
- Always escape user-generated content
- Validate content client-side before submission

## SEC-05: CSRF Protection

### Implementation
- `CSRFMiddleware` generates and validates tokens
- Token stored in cookie, sent in `X-CSRF-Token` header
- Constant-time comparison prevents timing attacks

### Usage
1. **Automatic**: Middleware sets `csrf_token` cookie on GET requests
2. **Required**: Client must include token in `X-CSRF-Token` header for POST/PUT/DELETE
3. **Validation**: Server compares header token with cookie token

### Frontend Integration
```javascript
// Get CSRF token from cookie
const csrfToken = document.cookie
  .split('; ')
  .find(row => row.startsWith('csrf_token='))
  ?.split('=')[1];

// Include in request headers
fetch('/api/endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRF-Token': csrfToken,
  },
  body: JSON.stringify(data),
});
```

## Authentication Security

### Password Requirements
- Minimum 8 characters
- Maximum 128 characters
- Must contain uppercase, lowercase, and numbers
- Validated with `validate_password_strength()`

### JWT Token Security
- Tokens signed with `SECRET_KEY`
- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- Tokens stored in httpOnly cookies (recommended) or localStorage

### Rate Limiting
- Login: 5 requests per 60 seconds
- Register: 3 requests per 60 seconds
- Prevents brute force attacks

## Input Validation

### Request Size Limits
- Max video upload: 500MB (configurable)
- Request body limits enforced by FastAPI
- Content-type validation on uploads

### File Upload Security
- Allowed video types validated
- File extensions checked
- MIME type verification
- Files stored outside web root

## Security Checklist

- [x] HTTPS enforcement
- [x] Security headers (CSP, X-Frame-Options, etc.)
- [x] CSRF protection
- [x] SQL injection prevention (ORM)
- [x] XSS prevention (output encoding, CSP)
- [x] Password strength validation
- [x] Rate limiting on auth endpoints
- [x] Input validation on all endpoints
- [x] File upload restrictions
- [x] Error handling (no sensitive data in errors)

## Reporting Security Issues

If you discover a security vulnerability, please report it privately to the development team. Do not disclose publicly until a fix is available.

---

*Security documentation updated: 2026-04-30*
