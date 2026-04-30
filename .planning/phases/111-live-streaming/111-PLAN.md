# Phase 111: Live Streaming Infrastructure

## Goal
Enhance existing live streaming with scheduling, DVR controls, real-time metrics, and notification system.

## Tasks

### 1. Backend Models
- [ ] Add LiveStreamSchedule model for scheduled streams
- [ ] Add LiveStreamDVR model for DVR segments
- [ ] Add LiveStreamNotification model for stream alerts

### 2. Backend Service
- [ ] Add schedule_stream() method
- [ ] Add get_upcoming_streams() method
- [ ] Add get_dvr_segments() method
- [ ] Add update_viewer_count() method
- [ ] Add subscribe_to_stream() method for notifications

### 3. Backend Routes
- [ ] POST /live/schedule - Schedule a stream
- [ ] GET /live/upcoming - Get scheduled streams
- [ ] GET /live/streams/{id}/dvr - Get DVR segments
- [ ] POST /live/streams/{id}/notify - Notify subscribers
- [ ] WebSocket /live/streams/{id}/ws - Real-time updates

### 4. Frontend Components
- [ ] StreamScheduleForm component
- [ ] UpcomingStreams component
- [ ] DVRControls component
- [ ] LiveNotifications component

### 5. Integration
- [ ] Update main.py with new routes
- [ ] Add WebSocket endpoint for real-time updates

## Files to Create/Modify
- backend/app/models/livestream.py (enhance)
- backend/app/services/livestream_service.py (enhance)
- backend/app/routes/livestream.py (enhance)
- frontend/src/components/Live/ScheduleForm.tsx (new)
- frontend/src/components/Live/DVRControls.tsx (new)
- frontend/src/api/livestream.ts (enhance)

## Success Criteria
- Creators can schedule streams in advance
- Viewers can see upcoming scheduled streams
- DVR allows seeking within live buffer
- Real-time viewer count updates via WebSocket
- Subscribers get notified when streams go live
