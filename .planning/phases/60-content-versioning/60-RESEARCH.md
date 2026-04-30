# Phase 60 Research: Content Versioning

## Research Summary

### Versioning Architecture

**Approach:** MovieVersion model linking to separate Video files
- Each movie can have multiple versions
- Each version has its own video file
- Shared metadata at movie level, version-specific metadata at version level

### Database Schema

**MovieVersion Model (New):**
- id: UUID
- movie_id: FK to Movie
- video_id: FK to Video
- version_type: string (theatrical, directors_cut, extended, etc.)
- version_name: string (display name)
- runtime_minutes: int
- content_warnings: JSON array
- is_default: boolean
- created_at: datetime

**Movie Model Extension:**
- default_version_id: FK to MovieVersion (nullable)

### Version Types (Predefined)

1. theatrical - Original theatrical release
2. directors_cut - Director cut version
3. extended - Extended edition
4. unrated - Unrated version
5. remastered - Remastered version

### Watch History Integration

**Approach:** Track history per version
- Extend WatchHistory with version_id field
- Separate progress tracking per version
- Resume picks up from last watched version

### Frontend UX

**Version Selection:**
- Dropdown on movie detail page
- Badge indicating available versions
- Default version pre-selected
- Remember last watched version per user

**Version Metadata Display:**
- Runtime comparison
- Content warnings specific to version
- Version description

## Technical Decisions

1. **Separate Video per Version:** Each version has its own video file
   - Reason: Clean separation, independent transcoding
   - Trade-off: More storage used

2. **Version-Specific Watch History:** Separate progress per version
   - Reason: Users may watch different versions
   - Trade-off: More history records

3. **Default Version at Movie Level:** One default for all users
   - Reason: Simple, predictable
   - Trade-off: No per-user default

---
*Research completed: 2026-04-30*
