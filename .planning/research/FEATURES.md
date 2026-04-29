# Feature Research: CC Video

## Table Stakes

### Authentication

- User can register or be created and then log in.
- User session persists across refresh.
- User can log out.
- Admin access is role-protected.

### Movie Catalog

- User can view a list of available movies.
- User can see movie title, cover/poster placeholder, description, and duration/status when available.
- User can open a movie detail or playback page.

### Playback

- User can play an uploaded movie in the browser.
- Backend supports browser video playback, including range requests where needed.
- User cannot play videos without valid access.

### Admin Movie Management

- Admin can create movie records.
- Admin can upload local video files.
- Admin can edit movie metadata.
- Admin can remove or disable movies.
- Admin can see upload/processing status, even if v1 has no transcoding.

## Differentiators Deferred From v1

- Personalized recommendations.
- Favorites/watch history.
- Comments or ratings.
- Subtitles and multiple audio tracks.
- Adaptive bitrate streaming.
- Payment or membership tiers.

## Anti-Features

- Anonymous public video access conflicts with the confirmed login requirement.
- External video URL ingestion conflicts with the confirmed local upload requirement.
- Native mobile clients would distract from the web-first v1.

## Complexity Notes

Upload and playback are the riskiest v1 features because large files, MIME validation, storage paths, and browser range requests must work together. Admin CRUD and catalog browsing are straightforward once authentication and data models exist.
