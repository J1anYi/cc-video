# Phase 63 Research: Watch Parties

## Research Summary

### Watch Party Architecture

**Models:**
- WatchParty: id, movie_id, host_id, scheduled_time, is_public, status
- WatchPartyParticipant: id, party_id, user_id, joined_at
- WatchPartyChat: id, party_id, user_id, message, created_at

### Real-Time Features

**WebSocket Events:**
- party:join - User joins party
- party:leave - User leaves party
- party:sync - Host sends playback position
- party:chat - User sends message

### Playback Synchronization

- Host is the source of truth for playback state
- Play/pause/seek events broadcast to all participants
- Participants sync to host position with small buffer

### API Endpoints

- POST /api/watch-parties - Create party
- POST /api/watch-parties/{id}/join - Join party
- POST /api/watch-parties/{id}/invite - Invite friends
- GET /api/watch-parties/public - List public parties

---
*Research completed: 2026-04-30*
