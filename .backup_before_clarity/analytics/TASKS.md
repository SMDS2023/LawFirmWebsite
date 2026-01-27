# Analytics Tasks

> **Project:** Website Analytics
> **Created:** 2025-12-12

---

## Backlog

### T-001: Configure GA4 Credentials
**Priority:** P0
**Status:** `pending`
**Type:** setup

Set up Google Analytics 4 API access.

**Acceptance Criteria:**
- [ ] Create Google Cloud project (or use existing)
- [ ] Enable Analytics Data API
- [ ] Create service account
- [ ] Download JSON key to `credentials/ga4_service_account.json`
- [ ] Add service account email as viewer in GA4 admin
- [ ] Update `config.yaml` with correct property ID
- [ ] Test API connection works

---

### T-002: Configure Clarity API
**Priority:** P0
**Status:** `pending`
**Type:** setup

Set up Microsoft Clarity API access.

**Acceptance Criteria:**
- [ ] Get API key from Clarity project settings
- [ ] Verify project ID is correct in config.yaml
- [ ] Test API returns actual data (not mock)
- [ ] Document API key storage method

---

### T-003: First Live Report
**Priority:** P1
**Status:** `pending`
**Type:** feature
**Blocked-by:** T-001, T-002

Generate first real weekly report with live data.

**Acceptance Criteria:**
- [ ] GA4 data shows real sessions/users
- [ ] Clarity data shows real behavior metrics
- [ ] Week-over-week deltas calculate correctly
- [ ] Report opens correctly in browser
- [ ] No mock data warnings in output

---

### T-004: Add Scheduled Execution
**Priority:** P2
**Status:** `pending`
**Type:** feature

Set up automatic weekly report generation.

**Acceptance Criteria:**
- [ ] Create Windows Task Scheduler task OR GitHub Action
- [ ] Runs every Monday at 8 AM
- [ ] Handles errors gracefully
- [ ] Sends notification on completion (optional)

---

### T-005: Add Email Distribution
**Priority:** P3
**Status:** `pending`
**Type:** feature

Send weekly reports via email.

**Acceptance Criteria:**
- [ ] Configure email settings (SMTP or API)
- [ ] Send HTML report as email body
- [ ] Add recipient list to config
- [ ] Test delivery

---

## Completed

(None yet)

---

*Last Updated: 2025-12-12*
