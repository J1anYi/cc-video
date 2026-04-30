# CC Video

## What This Is

CC Video is a web-based movie watching system with separated frontend and backend services. Regular users log in, browse a movie catalog, and play uploaded videos in the browser; administrators manage the movie library by uploading local video files and maintaining movie metadata.

The v1 product focused on making the basic viewing loop work end to end: a user can log in, find a movie in the list, and watch it, while an administrator can add and manage the movies that appear there.

## Current State: v2.8 Planning (2026-04-30)

**v2.7 Advanced Security and Compliance shipped.** Starting v2.8 Advanced Media and Streaming Enhancements.

## Core Value

Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Current Milestone: v2.8 Advanced Media and Streaming Enhancements

**Goal:** Enhance video streaming with adaptive bitrate, HDR support, advanced codecs, and improved media processing.

**Target features:**
- Adaptive bitrate streaming (HLS/DASH)
- HDR video support
- Advanced audio tracks (multi-language, surround sound)
- Video chapters and bookmarks
- Improved transcoding pipeline

## Requirements

### Validated (v1.0-v1.10)

- [x] Core MVP features (auth, catalog, playback, admin)
- [x] Search and filtering (v1.1)
- [x] Watch history and favorites (v1.2)
- [x] Poster images and subtitles (v1.3)
- [x] Password reset and profile management (v1.4)
- [x] Personalized recommendations (v1.5)
- [x] Ratings, reviews, comments (v1.6)
- [x] Social features (v1.7)
- [x] Watchlists (v1.8)
- [x] Admin and safety (v1.9)
- [x] Analytics and insights (v1.10)

### Validated (v2.0-v2.7)

- [x] Platform maturity (v2.0)
- [x] Enhanced UX (v2.1)
- [x] Monetization (v2.2)
- [x] Enterprise (v2.3)
- [x] AI/ML (v2.4)
- [x] Advanced content management (v2.5)
- [x] Community and engagement (v2.6)
- [x] Advanced security and compliance (v2.7)

### Active (v2.8)

- [ ] Adaptive bitrate streaming
- [ ] HDR video support
- [ ] Advanced audio tracks
- [ ] Video chapters and bookmarks
- [ ] Enhanced transcoding pipeline

## Context

v2.8 enhances media capabilities with adaptive streaming, HDR support, multi-language audio, video chapters, and an improved transcoding pipeline for premium viewing experiences.

## Constraints

- **Architecture**: Frontend and backend must be separated
- **Video source**: Administrator-uploaded local video files
- **Authentication**: Regular user login is required
- **Web-first**: Browser-based viewing experience

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-04-30 - Starting v2.8*
