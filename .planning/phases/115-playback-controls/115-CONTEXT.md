# Phase 115: Advanced Playback Controls

## Goal
Implement playback speed control, frame-by-frame navigation, picture-in-picture, and watch position sync.

## Requirements
- APC-01: Playback speed control (0.5x to 2x)
- APC-02: Frame-by-frame navigation
- APC-03: Picture-in-picture mode
- APC-04: Keyboard shortcuts configuration
- APC-05: Watch position sync across devices

## Scope

### Backend
- PlaybackSettings model for user preferences
- WatchProgress model for position sync
- PlaybackSettingsService
- Playback endpoints

### Frontend
- PlaybackSpeedControl component
- PiP toggle component
- Keyboard shortcuts manager

## Success Criteria
- Playback speed control (0.5x-2x)
- Frame-by-frame navigation
- Picture-in-picture support
- Watch position synced
