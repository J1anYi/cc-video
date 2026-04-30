# Phase 72 Context: HDR Video Support

**Phase:** 72
**Milestone:** v2.8 Advanced Media & Streaming Enhancements
**Status:** Planning

## Goal

Add HDR video detection and playback support for compatible devices with SDR fallback for non-HDR devices.

## Requirements

- **HDR-01**: System detects HDR content on upload
- **HDR-02**: Player supports HDR10 playback on compatible devices
- **HDR-03**: System generates SDR fallback for non-HDR devices
- **HDR-04**: User preference for HDR when available
- **HDR-05**: HDR metadata preserved during transcoding

## Success Criteria

1. HDR content detected on upload
2. HDR10 playback on compatible devices
3. SDR fallback generated automatically
4. User HDR preference stored
5. HDR metadata preserved

## Technical Context

### HDR Formats
- HDR10: Most common, static metadata
- HDR10+: Dynamic metadata (optional future)
- Dolby Vision: Proprietary (out of scope)

### Detection Methods
- FFprobe: `color_transfer`, `color_primaries`, `color_space`
- HDR10: `smpte2084` transfer function, `bt2020` primaries

### Fallback Generation
- Tone mapping using FFmpeg filters
- zscale or tonemap filter for conversion

## Dependencies

- Phase 71: HLS streaming infrastructure
- FFmpeg with HDR support
- Browser HDR support detection

## Out of Scope

- Dolby Vision support
- HDR10+ dynamic metadata
- HLG (Hybrid Log-Gamma)
