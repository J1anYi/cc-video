# Plan: Phase 124 - Access Control

## Goal
Implement access control with content permissions, time windows, device limits, and stream management.

## Tasks

### 1. Database Models
- AccessLevel, TimeWindowType, PermissionType enums
- AccessPolicy, ContentPermission, TimeWindow, DeviceLimit, StreamSession models

### 2. Service Layer
- AccessControlService with policy management, permission checks, session tracking

### 3. API Routes
- 6 endpoints for access control operations

### 4. Schemas
- Request/Response schemas

### 5. Frontend API
- access.ts

### 6. Integration
- Register router in main.py

## Success Criteria
All 5 AC requirements implemented
