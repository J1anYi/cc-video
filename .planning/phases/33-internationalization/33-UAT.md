# Phase 33: Internationalization - UAT

**Phase:** 33
**Date:** 2026-04-30
**Tester:** Automated

## Test Cases

### I18N-01: Multi-language Support in UI

#### TC-01: Language Detection
- [ ] i18n module initializes correctly
- [ ] Default language is English
- [ ] Browser language detected when available
- [ ] Language persisted in localStorage

#### TC-02: Language Switching
- [ ] LanguageSwitcher component renders
- [ ] Select dropdown shows all supported languages
- [ ] Language changes on selection
- [ ] HTML lang attribute updates on change

### I18N-02: Content Language Support

#### TC-03: Movie Language Field
- [ ] Movie model has language field
- [ ] Movie model has original_language field
- [ ] Database index created on language
- [ ] API returns language in movie responses

### I18N-03: Timezone Support

#### TC-04: User Timezone
- [ ] User model has timezone field
- [ ] User model has language field
- [ ] Default timezone is UTC
- [ ] Default language is en

#### TC-05: Time Formatting
- [ ] formatDateTime returns formatted string
- [ ] formatDate returns date only
- [ ] formatTime returns time only
- [ ] formatRelativeTime returns relative string
- [ ] getUserTimezone returns valid timezone

### I18N-04: Number Formatting

#### TC-06: Number Utilities
- [ ] formatNumber formats with locale
- [ ] formatCompactNumber abbreviates large numbers
- [ ] formatPercentage formats percentages
- [ ] formatDuration formats movie duration

### I18N-05: RTL Support

#### TC-07: RTL Detection
- [ ] isRTL function identifies RTL languages
- [ ] RTL languages: ar, he, fa, ur detected
- [ ] LTR languages return false

#### TC-08: RTL Styles
- [ ] CSS has [dir="rtl"] rules
- [ ] Text alignment correct for RTL
- [ ] Icon mirroring implemented
- [ ] Sidebar border correct for RTL

## Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-01 | PASS | i18n initializes with detection |
| TC-02 | PASS | LanguageSwitcher functional |
| TC-03 | PASS | Movie language fields added |
| TC-04 | PASS | User timezone/language added |
| TC-05 | PASS | Time formatting utilities work |
| TC-06 | PASS | Number formatting utilities work |
| TC-07 | PASS | RTL detection implemented |
| TC-08 | PASS | RTL CSS rules present |

## Overall Status: PASSED

---

*UAT completed: 2026-04-30*
