# PLAN: Phase 21 - Admin User Management

**Milestone:** v1.9 Admin & Safety
**Phase:** 21
**Created:** 2026-04-30

## Goal

Implement admin user management dashboard with capabilities to list, search, view, suspend, and delete user accounts.

## Requirements

- **ADMIN-USER-01**: Admin can list all users with pagination
- **ADMIN-USER-02**: Admin can search users by email or username
- **ADMIN-USER-03**: Admin can view user details (profile, activity, stats)
- **ADMIN-USER-04**: Admin can suspend/unsuspend user accounts
- **ADMIN-USER-05**: Admin can delete user accounts (soft delete)

## Context

- Existing admin panel at `/admin/movies` for movie management
- User model already exists with `is_admin` field
- Need to extend admin capabilities to user management
- Suspended users should not be able to login
- Soft delete preserves data integrity

## Implementation Plan

### Task 1: Backend - User Admin Endpoints

**File:** `backend/app/routes/admin_users.py`

Create admin-only endpoints:
- `GET /api/admin/users` - List users with pagination
- `GET /api/admin/users?search=<query>` - Search users
- `GET /api/admin/users/{user_id}` - Get user details
- `PATCH /api/admin/users/{user_id}/suspend` - Suspend/unsuspend user
- `DELETE /api/admin/users/{user_id}` - Soft delete user

**Schema additions** (`backend/app/schemas/user.py`):
- `UserAdminView` - Full user details for admin
- `UserListResponse` - Paginated user list
- `UserSuspensionRequest` - Suspend/unsuspend request

**Model changes** (`backend/app/models/user.py`):
- Add `is_suspended` boolean field
- Add `deleted_at` timestamp for soft delete

### Task 2: Backend - User Admin Service

**File:** `backend/app/services/admin_user.py`

Implement service methods:
- `list_users(page, limit, search)` - Paginated user list
- `get_user_details(user_id)` - User with activity stats
- `suspend_user(user_id, suspend)` - Toggle suspension
- `delete_user(user_id)` - Soft delete (set deleted_at)

### Task 3: Frontend - Admin Users Page

**File:** `frontend/src/routes/admin/Users.tsx`

Create admin users management page:
- User list table with pagination
- Search input for filtering
- User detail modal/drawer
- Suspend/unsuspend button
- Delete button with confirmation

### Task 4: Frontend - Admin Users API Client

**File:** `frontend/src/api/adminUsers.ts`

Create API client methods:
- `getUsers(page, limit, search)`
- `getUserDetails(userId)`
- `suspendUser(userId, suspend)`
- `deleteUser(userId)`

### Task 5: Update Authentication for Suspended Users

**File:** `backend/app/routes/auth.py`

Modify login to check `is_suspended` and `deleted_at`:
- Return error if user is suspended
- Return error if user is deleted

## Dependencies

- Phase 1: Backend Foundation (User model)
- Phase 6: User Registration (Auth system)

## Verification Criteria

- [ ] Admin can view paginated list of all users
- [ ] Admin can search users by email or username
- [ ] Admin can view detailed user information
- [ ] Admin can suspend a user (user cannot login)
- [ ] Admin can unsuspend a user (user can login again)
- [ ] Admin can soft delete a user
- [ ] Suspended users see appropriate error on login
- [ ] Deleted users see appropriate error on login

## Files Changed

### Created
- backend/app/routes/admin_users.py
- backend/app/services/admin_user.py
- frontend/src/routes/admin/Users.tsx
- frontend/src/api/adminUsers.ts

### Modified
- backend/app/models/user.py
- backend/app/schemas/user.py
- backend/app/main.py
- backend/app/routes/auth.py
- frontend/src/App.tsx

---
*Plan created: 2026-04-30*
