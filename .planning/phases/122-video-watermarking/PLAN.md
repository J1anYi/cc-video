# Plan: Phase 122 - Video Watermarking

## Goal
Implement video watermarking with visible overlays, forensic marking, and leak tracing.

## Tasks

### 1. Database Models
- WatermarkType enum (VISIBLE, FORENSIC, USER_SPECIFIC)
- WatermarkPosition enum (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, CENTER, CUSTOM)
- WatermarkConfiguration model
- Watermark model
- WatermarkSession model
- ForensicWatermark model
- LeakTrace model

### 2. Service Layer
- WatermarkService with configure, create, apply, generate_forensic, trace_leak methods

### 3. API Routes
- 7 endpoints for watermark operations

### 4. Schemas
- Request/Response schemas

### 5. Frontend API
- watermark.ts

### 6. Integration
- Register router in main.py

## Success Criteria
All 5 VW requirements implemented
