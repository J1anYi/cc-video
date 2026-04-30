# Phase 95: Custom Report Builder - Context

**Gathered:** 2026-04-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement customizable reporting tools for generating, scheduling, and exporting reports.

**Delivers:**
- Custom report builder
- Scheduled report generation
- Report export (PDF, CSV, Excel)
- Report sharing and permissions
- Dashboard customization

</domain>

<decisions>
### Data Model
- ReportDefinition, ReportSchedule, ReportExecution, DashboardConfig models

### API Endpoints
- POST /admin/reports - Create report
- GET /admin/reports - List reports
- GET /admin/reports/{id} - Get report
- POST /admin/reports/{id}/execute - Execute report
- GET /admin/reports/{id}/export - Export report
- POST /admin/reports/{id}/schedule - Schedule report

</decisions>

---

*Phase: 095-custom-report-builder*
