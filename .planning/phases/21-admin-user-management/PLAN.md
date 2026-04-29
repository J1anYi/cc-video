# PLAN: Phase 21 - Admin User Management

**Milestone:** v1.9 Admin & Safety
**Phase:** 21
**Goal:** Implement admin dashboard for user management

## Requirements

- ADMIN-USER-01: Admin can list all users with pagination
- ADMIN-USER-02: Admin can search users by email or username
- ADMIN-USER-03: Admin can view user details (profile, activity, stats)
- ADMIN-USER-04: Admin can suspend/unsuspend user accounts
- ADMIN-USER-05: Admin can delete user accounts (soft delete)

## Success Criteria

1. Admin can browse all users with pagination
2. Admin can search users by email or display name
3. Admin can view user profile with activity history
4. Admin can suspend/unsuspend accounts
5. Suspended users cannot log in

## Implementation Plan

### Task 1: Backend - User Status Field
- Add `is_suspended` field to User model
- Add `suspended_at` and `suspended_reason` fields
- Update user schema to include status

### Task 2: Backend - Admin User API
- GET /api/admin/users - List users with pagination and search
- GET /api/admin/users/{id} - Get user details
- PATCH /api/admin/users/{id}/suspend - Suspend user
- PATCH /api/admin/users/{id}/unsuspend - Unsuspend user
- DELETE /api/admin/users/{id} - Soft delete user

### Task 3: Backend - Auth Check
- Check is_suspended on login
- Return appropriate error message
- Clear tokens on suspension

### Task 4: Frontend - Admin Users Page
- Create /admin/users route
- User table with search and pagination
- Status badges (active, suspended)

### Task 5: Frontend - User Detail Modal
- Show user profile info
- Activity summary (reviews, comments, ratings)
- Suspend/unsuspend button
- Delete confirmation dialog

### Task 6: Frontend - Suspend Dialog
- Reason for suspension input
- Confirmation before action
- Success/error feedback

## Dependencies

- Existing User model
- Existing admin routes
- Existing auth system

## Risks

- Accidental admin suspension: Prevent suspending own account
- Data recovery: Soft delete allows recovery

---
*Phase plan created: 2026-04-30*
