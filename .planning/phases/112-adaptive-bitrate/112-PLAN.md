# Phase 112: Adaptive Bitrate Streaming

## Tasks

### 1. Backend Models
- [ ] AdaptiveStreamVariant model for quality variants
- [ ] BandwidthMetric model for analytics
- [ ] QualityPreference model for user preferences

### 2. Backend Service
- [ ] create_stream_variant() method
- [ ] get_variants_for_movie() method
- [ ] record_bandwidth_metric() method
- [ ] get_recommended_quality() method
- [ ] get_bandwidth_stats() method

### 3. Backend Routes
- [ ] POST /streaming/variants - Create variant
- [ ] GET /streaming/movies/{id}/variants - Get variants
- [ ] POST /streaming/metrics - Record bandwidth
- [ ] GET /streaming/stats - Get bandwidth stats

### 4. Frontend
- [ ] QualitySelector component
- [ ] BandwidthIndicator component
- [ ] Adaptive player configuration

### 5. Integration
- [ ] Update main.py with streaming routes

## Files to Create/Modify
- backend/app/models/streaming.py (new)
- backend/app/services/streaming_service.py (new)
- backend/app/routes/streaming.py (new)
- frontend/src/components/Player/QualitySelector.tsx (new)
- frontend/src/api/streaming.ts (new)

## Success Criteria
- Multiple quality variants per video
- Auto-switching based on bandwidth
- Manual quality selection
- Bandwidth analytics
