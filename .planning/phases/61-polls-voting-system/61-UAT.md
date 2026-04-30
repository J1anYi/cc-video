# Phase 61 UAT: Polls & Voting System

**Phase:** 61
**Date:** 2026-04-30
**Status:** PASSED

## Test Results

### POLL-01: Admin Creates Polls

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-01 | Create poll with options | PASS | Poll created with 3 options |
| TC-02 | Create poll with expiration | PASS | Poll expires on date |
| TC-03 | Link poll to movie | PASS | Poll appears on movie page |

### POLL-02: User Voting

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-04 | User votes on poll | PASS | Vote recorded successfully |
| TC-05 | User cannot vote twice | PASS | Error shown for duplicate vote |
| TC-06 | View after voting | PASS | Results shown after voting |

### POLL-03: Poll Results

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-07 | View results | PASS | Percentages displayed correctly |
| TC-08 | Multiple votes | PASS | Percentages update in real-time |
| TC-09 | Total count | PASS | Total votes shown |

### POLL-04: Expiration

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-10 | Poll expires | PASS | Poll closed, results frozen |
| TC-11 | Close poll early | PASS | Admin can close poll |

### POLL-05: Poll Display

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-12 | Poll on movie page | PASS | Poll widget shown on movie page |
| TC-13 | Community polls page | PASS | All active polls listed |

### POLL-06: Notifications

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-14 | New poll notification | PASS | Followers notified |
| TC-15 | Notification content | PASS | Poll title, movie name shown |

## Code Verified

- backend/app/models/poll.py - Poll model with options
- backend/app/routes/polls.py - Poll API endpoints
- frontend/src/components/PollWidget.tsx - Poll display component
- frontend/src/pages/admin/PollManagement.tsx - Admin poll management

## Integration

- Polls linked to movies
- Voting restricted to authenticated users
- Notifications for new polls

## Overall Status: PASSED

---

*UAT completed: 2026-04-30*
