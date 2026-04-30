# Phase 56 Research: Live Streaming Infrastructure

**Researched:** 2026-04-30
**Phase:** 56 - Live Streaming Infrastructure

## Technology Stack for Live Streaming

### Recommended Approach: HLS for Live

For this phase, **HLS is recommended** because:
- Already using HLS for VOD content
- Browser support is excellent
- Simpler implementation
- Acceptable latency for most live events (10-15 seconds)

### Backend Components Needed

1. **LiveStream Model**
   - title, description, scheduled_start, actual_start, end_time
   - status: scheduled, live, ended
   - stream_key (unique identifier)
   - viewer_count (real-time)

2. **Stream Ingest**
   - RTMP endpoint for receiving stream (ffmpeg/NGINX-RTMP)
   - Convert to HLS segments
   - Store segments temporarily

3. **HLS Playlist Generation**
   - Live playlist (sliding window)
   - Segment duration: 2-4 seconds
   - Playlist updates every segment

4. **Viewer Count Tracking**
   - WebSocket or SSE for real-time updates
   - Track active connections

### Frontend Components Needed

1. **Live Events Section**
   - Upcoming events list
   - Currently live indicator
   - Event detail page

2. **Live Video Player**
   - HLS.js for playback
   - Real-time viewer count display

3. **Admin Stream Management**
   - Schedule event form
   - Start/End stream controls

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| HLS for live streaming | Already in use for VOD, good browser support |
| WebSocket for viewer count | Real-time updates with low overhead |
| ffmpeg for transcoding | Industry standard, already in use |
