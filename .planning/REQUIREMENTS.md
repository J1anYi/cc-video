# Requirements: CC Video

**Defined:** 2026-04-30
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## v1.9 Requirements

Requirements for v1.9 Admin & Safety milestone. Enhances admin capabilities, content moderation, and user interactions.

### Admin User Management

- [x] **ADMIN-USER-01**: Admin can list all users with pagination
- [x] **ADMIN-USER-02**: Admin can search users by email or username
- [x] **ADMIN-USER-03**: Admin can view user details (profile, activity, stats)
- [x] **ADMIN-USER-04**: Admin can suspend/unsuspend user accounts
- [x] **ADMIN-USER-05**: Admin can delete user accounts (soft delete)

### Content Moderation

- [ ] **MOD-01**: User can report reviews for inappropriate content
- [ ] **MOD-02**: User can report comments for inappropriate content
- [ ] **MOD-03**: Admin can view reported content queue
- [ ] **MOD-04**: Admin can dismiss reports (content is acceptable)
- [ ] **MOD-05**: Admin can remove reported content
- [ ] **MOD-06**: Admin can issue warnings to users

### Advanced Search

- [ ] **SEARCH-01**: User can filter movies by minimum rating
- [ ] **SEARCH-02**: User can filter movies by release year range
- [ ] **SEARCH-03**: User can filter movies by duration range
- [ ] **SEARCH-04**: User can combine multiple filters
- [ ] **SEARCH-05**: User can sort search results (rating, year, title)

### User Blocking

- [ ] **BLOCK-01**: User can block another user
- [ ] **BLOCK-02**: User can unblock a blocked user
- [ ] **BLOCK-03**: Blocked user's content is hidden from blocker
- [ ] **BLOCK-04**: Blocked user cannot comment on blocker's reviews
- [ ] **BLOCK-05**: User can view their blocked users list

### @Mentions

- [ ] **MENTION-01**: User can @mention other users in comments
- [ ] **MENTION-02**: User can @mention other users in reviews
- [ ] **MENTION-03**: Mentioned user receives notification
- [ ] **MENTION-04**: @mention links to mentioned user's profile
- [ ] **MENTION-05**: @mention autocomplete suggests followed users

## Out of Scope

| Feature | Reason |
|---------|--------|
| IP-based bans | Requires additional infrastructure |
| Content auto-moderation | ML-based filtering deferred |
| Bulk user actions | Admin safety - single actions first |
| Audit logs | Deferred to admin dashboard milestone |
| Role-based permissions | Single admin role for v1.9 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ADMIN-USER-01 | Phase 21 | Complete |
| ADMIN-USER-02 | Phase 21 | Complete |
| ADMIN-USER-03 | Phase 21 | Complete |
| ADMIN-USER-04 | Phase 21 | Complete |
| ADMIN-USER-05 | Phase 21 | Complete |
| MOD-01 | Phase 22 | Pending |
| MOD-02 | Phase 22 | Pending |
| MOD-03 | Phase 22 | Pending |
| MOD-04 | Phase 22 | Pending |
| MOD-05 | Phase 22 | Pending |
| MOD-06 | Phase 22 | Pending |
| SEARCH-01 | Phase 23 | Pending |
| SEARCH-02 | Phase 23 | Pending |
| SEARCH-03 | Phase 23 | Pending |
| SEARCH-04 | Phase 23 | Pending |
| SEARCH-05 | Phase 23 | Pending |
| BLOCK-01 | Phase 24 | Pending |
| BLOCK-02 | Phase 24 | Pending |
| BLOCK-03 | Phase 24 | Pending |
| BLOCK-04 | Phase 24 | Pending |
| BLOCK-05 | Phase 24 | Pending |
| MENTION-01 | Phase 25 | Pending |
| MENTION-02 | Phase 25 | Pending |
| MENTION-03 | Phase 25 | Pending |
| MENTION-04 | Phase 25 | Pending |
| MENTION-05 | Phase 25 | Pending |

**Coverage:**
- v1.9 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-30*
*Last updated: 2026-04-30 - v1.9 milestone started*
