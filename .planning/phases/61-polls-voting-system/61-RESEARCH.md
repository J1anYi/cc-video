# Phase 61 Research: Polls & Voting System

## Research Summary

### Poll Architecture

**Approach:** Relational model for polls with options and votes
- Poll linked to Movie (optional) or standalone
- PollOption linked to Poll
- Vote links User to PollOption

### Database Schema

**Poll Model (New):**
- id: UUID
- movie_id: FK to Movie (nullable for general polls)
- title: string
- description: text (nullable)
- created_by: FK to User (admin)
- expires_at: datetime (nullable)
- is_active: boolean
- created_at: datetime

**PollOption Model (New):**
- id: UUID
- poll_id: FK to Poll
- option_text: string
- display_order: int

**PollVote Model (New):**
- id: UUID
- poll_id: FK to Poll
- option_id: FK to PollOption
- user_id: FK to User
- created_at: datetime

### API Endpoints

**Admin Endpoints:**
- POST /api/admin/polls - Create poll
- PUT /api/admin/polls/{id} - Update poll
- DELETE /api/admin/polls/{id} - Delete poll

**Public Endpoints:**
- GET /api/polls - List active polls
- GET /api/polls/{id} - Get poll details
- POST /api/polls/{id}/vote - Submit vote
- GET /api/polls/{id}/results - Get results

### Notification Integration

- Trigger: Admin creates poll linked to movie
- Recipients: Users following that movie
- Type: new_poll

---
*Research completed: 2026-04-30*
