# Phase 11 Summary: Password Reset

**Date:** 2026-04-29
**Status:** Complete

## What Was Built

Implemented email-based password reset functionality enabling users to recover access to their accounts.

## Backend Changes

### New Files
- `backend/app/models/password_reset.py` — PasswordReset model with token_hash, expires_at, used_at fields
- `backend/app/schemas/password_reset.py` — Request/Confirm/Response schemas
- `backend/app/services/email.py` — Email service with SMTP support and dev mode logging
- `backend/app/services/password_reset.py` — Token generation, validation, and password reset service

### Modified Files
- `backend/app/models/user.py` — Added password_resets relationship
- `backend/app/routes/auth.py` — Added POST /auth/password-reset and POST /auth/password-reset/confirm endpoints

## Frontend Changes

### New Files
- `frontend/src/routes/ForgotPassword.tsx` — Password reset request page
- `frontend/src/routes/ResetPassword.tsx` — Password reset confirmation page
- `frontend/src/api/passwordReset.ts` — API functions for password reset

### Modified Files
- `frontend/src/routes/Login.tsx` — Added "Forgot password?" link
- `frontend/src/App.tsx` — Added /forgot-password and /reset-password routes

## Security Features
- Tokens are 32-byte cryptographically secure random strings
- Tokens are hashed with SHA-256 before storage
- 1-hour token expiration
- Single-use tokens (marked as used after password reset)
- No email enumeration (always returns success message)

## Requirements Satisfied
- PWD-01: User can request password reset via email
- PWD-02: System sends email with secure reset link with expiration
- PWD-03: User can set new password via reset link
- PWD-04: Reset link invalidates after use or expiration

## Notes
- Email service works in development mode (logs to console) when SMTP_HOST is not configured
- Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM env vars for production email sending
- Set FRONTEND_URL env var to customize reset link URL (defaults to http://localhost:5173)
