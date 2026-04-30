# PLAN: Phase 33 - Internationalization

**Milestone:** v2.0 Platform Maturity
**Phase:** 33
**Goal:** Add multi-language support and localization

## Requirements

- I18N-01: Multi-language support in UI
- I18N-02: Content language detection and filtering
- I18N-03: Timezone-aware date/time display
- I18N-04: Currency and number formatting localization
- I18N-05: RTL (right-to-left) layout support

## Success Criteria

1. UI can be displayed in multiple languages
2. Users can select their preferred language
3. Dates and times show in user's timezone
4. Numbers formatted according to locale
5. RTL languages display correctly

## Implementation Plan

### Task 1: Backend - i18n Infrastructure
- Add language preference to User model
- Create translation file structure
- Implement language detection from headers
- Add language parameter to API responses

### Task 2: Backend - Content Language Support
- Add language field to Movie model
- Support multiple subtitle languages
- Implement language filtering in search
- Store content language metadata

### Task 3: Frontend - i18n Setup
- Integrate i18next or react-intl
- Create translation files for supported languages
- Implement language switcher component
- Store language preference in localStorage

### Task 4: Frontend - Translations
- Extract all UI strings
- Create English base translations
- Create translations for target languages
- Handle pluralization rules

### Task 5: Frontend - Timezone Support
- Detect user timezone
- Convert all dates/times to user timezone
- Store and display timezone in profile
- Handle timezone in notifications

### Task 6: Frontend - Number Formatting
- Implement locale-aware number formatting
- Format large numbers (1K, 1M)
- Handle decimal separators per locale
- Format percentages correctly

### Task 7: Frontend - RTL Support
- Add RTL stylesheet support
- Mirror layouts for RTL languages
- Test with Arabic/Hebrew content
- Ensure icons and arrows flip correctly

### Task 8: Backend - Translated Content
- Support movie metadata in multiple languages
- Translate category names
- Handle multi-language search
- Return appropriate language version

## Dependencies

- Translation resources
- Language detection libraries

## Risks

- Translation quality and maintenance
- Mitigation: Start with English and one other language, expand gradually

---
*Phase plan created: 2026-04-30*
