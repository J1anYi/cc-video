# Phase 58 Research: Content Scheduling System

## Research Summary

### Scheduling Architecture

**Approach:** Time-based content visibility
- Add availability_start and availability_end to Movie model
- Background task checks and updates content visibility
- Admin calendar view for schedule management

### Database Schema Extensions

**Movie Model Extensions:**
- availability_start: datetime (nullable, when content becomes visible)
- availability_end: datetime (nullable, when content expires)
- is_scheduled: boolean (true if scheduling is active)

### Scheduling Logic

**Content States:**
1. Scheduled (before availability_start): Hidden from catalog
2. Available (between start and end): Visible in catalog
3. Expired (after availability_end): Hidden from catalog
4. Permanent (no dates): Always visible (default behavior)

### Background Task

**Scheduled Task: Availability Manager**
- Runs every 5 minutes
- Checks movies with is_scheduled=true
- Updates visibility based on current time
- Sends notifications for newly available content

### Frontend Components

**User Features:**
- Countdown timer on scheduled content
- Coming Soon section for upcoming content
- Last Chance section for expiring content

**Admin Features:**
- Content calendar view
- Bulk scheduling
- Schedule conflict detection

## Technical Decisions

1. **Null = Always Available:** If dates are null, content is always visible
   - Reason: Backward compatible, no migration impact
   - Trade-off: Cannot schedule permanent content removal

2. **5-minute Task Interval:** Balance between responsiveness and resource usage
   - Reason: Content scheduling does not need second-precision
   - Trade-off: Up to 5-minute delay in visibility changes

3. **Soft Visibility:** Content hidden via query filter, not deleted
   - Reason: Admin can still see and manage scheduled content
   - Trade-off: Query complexity increases

---
*Research completed: 2026-04-30*
