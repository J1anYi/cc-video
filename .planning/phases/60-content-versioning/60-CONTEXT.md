# Phase 60 Context: Content Versioning

**Phase:** 60
**Milestone:** v2.5 Advanced Content Management and Live Streaming
**Status:** Planning

## Goal

Support multiple versions per movie with separate metadata and watch history.

## Requirements

- **VER-01**: Admin can create multiple versions of a movie (theatrical, director cut, extended)
- **VER-02**: User can select which version to watch from movie detail page
- **VER-03**: Each version maintains separate watch history
- **VER-04**: Admin can set default version for new viewers
- **VER-05**: Version metadata includes runtime differences and content warnings

## Success Criteria

1. Admin can create multiple versions of a movie (theatrical, director cut, extended)
2. Users can select which version to watch from movie detail page
3. Each version maintains separate watch history
4. Admin can set default version for new viewers
5. Version metadata includes runtime differences and content warnings

## Technical Context

### Existing Architecture
- Backend: FastAPI with SQLAlchemy
- Frontend: React with TypeScript
- Video: HLS streaming with multiple quality variants
- Database: SQLite (development), PostgreSQL (production)

### Integration Points
- Movie model for content metadata
- Video model for file storage
- WatchHistory model for tracking
- Phase 59 VideoVariant for quality variants

## Out of Scope

- Version comparison features
- Version-specific subtitles
- Version-specific posters

---
*Context created: 2026-04-30*
