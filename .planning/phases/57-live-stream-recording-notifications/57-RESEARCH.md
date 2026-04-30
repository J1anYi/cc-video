# Phase 57 Research: Live Stream Recording and Notifications

## Research Summary

### Live Stream Recording Architecture

**Approach:** HLS Segment Archival
- During live streaming, HLS segments are already being generated
- Archive segments to persistent storage when stream ends
- Generate VOD playlist from archived segments
- Create Movie record linking to archived stream

### Recording Storage Strategy

File Structure:
- backend/uploads/recordings/{stream_id}/playlist.m3u8
- backend/uploads/recordings/{stream_id}/segment_*.ts

### Live Event Notifications

**Notification Types:**
1. Upcoming Event: Sent 30 min and 5 min before scheduled start
2. Stream Starting: Sent when admin starts the stream
3. Recording Available: Sent when recording is ready for VOD

**User Follow System:**
- Users can follow live events
- Following triggers notifications for that event

### Database Schema Extensions

**LiveStream Model Extensions:**
- recording_path: Path to archived recording
- recording_movie_id: FK to Movie
- notification_sent: Track notification status

**LiveEventFollow Model (New):**
- user_id, live_stream_id, created_at
- notify_before_minutes: default 30

### API Endpoints

- POST /api/live/{stream_id}/follow
- DELETE /api/live/{stream_id}/follow
- GET /api/live/{stream_id}/recording

### Background Tasks

- Notification Dispatcher: Runs every minute, checks upcoming events
- Recording Processor: Finalizes recording on stream end

## Technical Decisions

1. HLS segments archived directly (no re-encoding) - fastest to VOD
2. Notification timing: 30 min, 5 min, at start
3. Explicit follow required for notifications

---
*Research completed: 2026-04-30*
