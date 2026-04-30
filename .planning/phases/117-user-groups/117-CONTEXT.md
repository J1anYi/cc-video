# Phase 117: User Groups and Clubs - Context

**Gathered:** 2026-05-01
**Status:** Ready for planning
**Source:** ROADMAP.md requirements

<domain>
## Phase Boundary

Implement user group functionality allowing users to create and manage groups, collections, and discussions.

**Delivers:**
- Public and private group creation
- Group membership management (join, leave, invite)
- Group-specific content collections
- Group discussion boards
- Group activity feeds

**Out of scope:**
- Watch parties (Phase 118)
- Social feeds (Phase 119)
- Gamification features (Phase 120)

</domain>

<decisions>
## Implementation Decisions

### Data Models
- **Group model**: id, tenant_id, name, slug, description, privacy (public/private), created_by, created_at, updated_at
- **GroupMember model**: id, group_id, user_id, role (owner/admin/member), joined_at
- **GroupCollection model**: id, group_id, name, description, created_by
- **GroupCollectionItem model**: id, collection_id, movie_id, added_by, added_at
- **GroupDiscussion model**: id, group_id, title, content, created_by, created_at, is_pinned, is_locked
- **GroupDiscussionReply model**: id, discussion_id, content, created_by, created_at
- **GroupActivity model**: id, group_id, user_id, activity_type, content, created_at

### API Endpoints
- `POST /groups` - Create group
- `GET /groups` - List groups (public + user's private)
- `GET /groups/{id}` - Get group details
- `PUT /groups/{id}` - Update group (admin only)
- `DELETE /groups/{id}` - Delete group (owner only)
- `POST /groups/{id}/join` - Join group
- `POST /groups/{id}/leave` - Leave group
- `POST /groups/{id}/invite` - Invite user to group
- `GET /groups/{id}/members` - List members
- `PUT /groups/{id}/members/{userId}` - Update member role
- `DELETE /groups/{id}/members/{userId}` - Remove member
- `GET /groups/{id}/collections` - List group collections
- `POST /groups/{id}/collections` - Create collection
- `POST /groups/{id}/collections/{collectionId}/items` - Add item to collection
- `DELETE /groups/{id}/collections/{collectionId}/items/{itemId}` - Remove item
- `GET /groups/{id}/discussions` - List discussions
- `POST /groups/{id}/discussions` - Create discussion
- `POST /groups/{id}/discussions/{discussionId}/replies` - Reply to discussion
- `GET /groups/{id}/activity` - Get activity feed

### Roles and Permissions
- **Owner**: Full control, can delete group, transfer ownership
- **Admin**: Can manage members, collections, moderate discussions
- **Member**: Can view, participate in discussions, add to collections (if allowed)

### Claude's Discretion
- Frontend component structure and styling
- Activity feed aggregation logic
- Notification integration for group events

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Patterns
- `backend/app/models/forum.py` — Forum model patterns (similar to groups)
- `backend/app/services/forum_service.py` — Service layer patterns
- `backend/app/routes/forum.py` — Route patterns
- `backend/app/models/movie.py` — Movie model for collection items

</canonical_refs>

<specifics>
## Specific Ideas

- Groups can have cover images and icons
- Activity feed shows: new members, new discussions, new collection items
- Private groups require invitation or approval to join
- Group slugs must be unique per tenant

</specifics>

<deferred>
## Deferred Ideas

- Group events and calendar (future phase)
- Group-specific live streams (future phase)
- Group analytics and insights (future phase)

</deferred>

---

*Phase: 117-user-groups*
*Context gathered: 2026-05-01*
