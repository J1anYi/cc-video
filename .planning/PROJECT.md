# CC Video

## What This Is

CC Video is a web-based movie watching system with separated frontend and backend services. Regular users log in, browse a movie catalog, and play uploaded videos in the browser; administrators manage the movie library by uploading local video files and maintaining movie metadata.

The v1 product focused on making the basic viewing loop work end to end: a user can log in, find a movie in the list, and watch it, while an administrator can add and manage the movies that appear there.

## Current State: v2.6 Planning (2026-04-30)

**v2.5 Advanced Content Management & Live Streaming shipped.** Starting v2.6 Community & Engagement Features.

The system now supports:
- User authentication with password reset
- Movie browsing, search, and filtering
- Video playback with subtitles and poster images
- Watch history and favorites
- User profile management
- Personalized recommendations
- Continue watching
- Trending movies
- Related movies
- Movie ratings and reviews
- Comments on reviews
- Helpful votes on reviews
- User following system
- Activity feed
- Notifications
- Social profiles
- User watchlists (public/private)
- Public watchlist discovery
- Auto-notifications for social events
- Admin user management
- Content moderation
- Advanced search filters
- User blocking
- @mentions
- User analytics dashboard
- Content performance metrics
- Admin dashboard enhancement
- Social analytics
- Recommendation insights
- Performance optimization
- Scalability improvements
- Internationalization (i18n)
- Security hardening
- Production readiness
- Accessibility (WCAG 2.1 AA)
- Advanced personalization
- PWA/offline support
- Advanced media features
- Premium user features
- Subscription system
- Payment integration (Stripe)
- Access control
- Admin business tools
- Business intelligence
- Public API platform
- Third-party integrations
- Enterprise features
- Developer tools
- Platform extensibility
- ML recommendation engine
- Content analysis
- Natural language processing
- Predictive analytics
- Automated workflows
- Live streaming infrastructure
- Live stream recording & notifications
- Content scheduling system
- Advanced video management
- Content versioning

## Core Value

Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Current Milestone: v2.6 Community & Engagement Features

**Goal:** Enhance community interaction with polls, quizzes, events, and gamification elements to boost user engagement.

**Target features:**
- Movie polls and voting system
- Movie trivia quizzes
- Virtual watch parties
- User achievements and badges
- Leaderboards and gamification

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
- [x] Admin & safety (v1.9)
- [x] Analytics & insights (v1.10)

### Validated (v2.0-v2.5)

- [x] Platform maturity - performance, scalability, i18n, security (v2.0)
- [x] Enhanced UX - accessibility, personalization, PWA (v2.1)
- [x] Monetization - subscriptions, payments, access control (v2.2)
- [x] Enterprise - API platform, integrations, developer tools (v2.3)
- [x] AI/ML - recommendations, NLP, predictive analytics (v2.4)
- [x] Advanced content management & live streaming (v2.5)

### Active (v2.6)

- [ ] Polls and voting system
- [ ] Movie trivia quizzes
- [ ] Virtual watch parties
- [ ] User achievements and badges
- [ ] Leaderboards and gamification

## Context

v1.0-v1.10 established the core platform with social features, admin tools, and analytics.

v2.0 added platform maturity with performance optimization, scalability, internationalization, and security hardening.

v2.1 enhanced user experience with accessibility (WCAG 2.1 AA), advanced personalization, PWA/offline support, and premium user features.

v2.2 added monetization with subscription tiers, Stripe payment integration, access control, and business intelligence.

v2.3 enabled enterprise features with public API platform, third-party integrations, developer tools, and platform extensibility.

v2.4 brought AI/ML capabilities with recommendation engines, content analysis, NLP, predictive analytics, and automated workflows.

v2.5 introduced live streaming and advanced content management, enabling real-time viewer engagement and sophisticated content operations.

v2.6 focuses on community engagement with interactive polls, quizzes, watch parties, and gamification to increase user retention and platform stickiness.

## Constraints

- **Architecture**: Frontend and backend must be separated - this is an explicit project requirement.
- **Video source**: v1 movie content comes from administrator-uploaded local video files - external video URLs are out of scope.
- **Authentication**: Regular user login is required for viewing - anonymous viewing is not the initial model.
- **Web-first**: The viewing experience is delivered through a browser - native apps are deferred.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build as separated frontend and backend | Explicit user requirement and a clean fit for web video catalog/API boundaries | Validated |
| Require ordinary user login for viewing | User confirmed login is required | Validated |
| Support administrator-uploaded local videos in v1 | User confirmed uploaded local video files are the source of movie content | Validated |
| Include admin movie management in v1 | User confirmed backend movie management is part of the core scope | Validated |
| Add search before advanced discovery features | Search is table stakes for any catalog; filtering can follow | Validated |
| Add self-registration before password reset | Registration enables organic growth; password reset is support for existing users | Validated |
| Add watch history before recommendations | History is personal data; recommendations require more signals | Validated |
| Add favorites before watch history | Favorites are explicit user intent; history is passive | Validated |
| Add poster images before subtitles | Visual catalog first; accessibility enhancement follows | Validated |
| Use SHA-256 hash for reset tokens | Secure, no plaintext tokens stored | Validated |
| 1-hour token expiration | Balance security and usability | Validated |
| No email enumeration | Prevent account discovery attacks | Validated |
| Content-based filtering by category | Simple, effective, no ML needed | Validated |
| 7-day window for trending | Balance freshness with data volume | Validated |
| Hide recommendations when filters active | User intent is search, not discovery | Validated |
| Single admin role for v1.9 | Simpler implementation, defer RBAC | Validated |
| Stripe for payment processing | Industry standard, comprehensive API | Validated |
| PWA for offline support | Web-first approach, no native app | Validated |
| WCAG 2.1 AA for accessibility | Standard compliance level | Validated |

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-04-30 - Starting v2.6*
