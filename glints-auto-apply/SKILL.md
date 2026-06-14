---
name: glints-auto-apply
description: "Use when searching or auto-applying to jobs on Glints Indonesia. Reverse-engineered Glints API — login, search (GraphQL), upload CV, and apply (REST) via CloakBrowser stealth Chromium. Use whenever user mentions Glints, job scanning, auto-apply, or wants to apply to Indonesian jobs programmatically."
version: 1.0.0
author: AL KINDI
license: MIT
metadata:
  hermes:
    tags: [glints, jobs, auto-apply, indonesia, career, automation, cloakbrowser]
    related_skills: [deep-research, content-intelligence]
---

# Glints Auto-Apply

Automate job search and application on Glints Indonesia via reverse-engineered API + CloakBrowser stealth Chromium.

## Overview

Glints uses Cloudflare WAF + bot detection. Regular curl and standard headless browsers are blocked. CloakBrowser (stealth Chromium with C++ source patches) bypasses all protection — 30/30 bot detection tests passed.

The apply flow is **NOT GraphQL** (common misconception). It's a REST API endpoint. The GraphQL is only used for job search.

## When to Use

- User wants to search legal/professional jobs on Glints
- User wants to auto-apply to multiple Glints jobs
- User mentions "Glints", "job scanning", "auto-apply"
- Career agent needs to scan Indonesian job portals

**Don't use for:**
- JobStreet, Indeed, Kalibrr (different APIs)
- Non-Indonesian job portals
- Manual browser-based applications (use browser tools instead)

## Prerequisites

- CloakBrowser installed: `pip install cloakbrowser` (already on this machine)
- Glints account credentials (email + password)
- CV PDF file ready

## API Endpoints (Reverse-Engineered)

### 1. Login — OAuth2 Password Grant

```
POST https://glints.com/api/oauth2/token
Content-Type: application/json

{
  "grant_type": "password",
  "client_id": "2f58c66702c29b821efec58b84e1aa84ee2d2a03a3bd2df8aea61fcd5e5ca50d",
  "username": "<email>",
  "password": "<password>"
}
```

Response:
```json
{
  "access_token": "eyJhbG...",
  "token_type": "Bearer",
  "activeRole": "CANDIDATE",
  "isAuthenticated": true
}
```

**Important:** `client_id` is a public client (no secret needed). The access_token is a Bearer token valid for the session.

### 2. Search Jobs — GraphQL

```
POST https://glints.com/api/v2-alc/graphql?op=searchJobsV3
Content-Type: application/json
Authorization: Bearer <token>

{
  "operationName": "searchJobsV3",
  "variables": {
    "data": {
      "SearchTerm": "legal associate",
      "CountryCode": "ID",
      "includeExternalJobs": true,
      "pageSize": 30,
      "page": 1
    }
  },
  "query": "query searchJobsV3($data: JobSearchConditionInput!) { searchJobsV3(data: $data) { jobsInPage { id title company { name } city { name } salaries { minAmount maxAmount CurrencyCode } isApplied type educationLevel minYearsOfExperience maxYearsOfExperience workArrangementOption } hasMore } }"
}
```

### 3. Apply — REST API (NOT GraphQL!)

```
POST https://glints.com/api/v2/v2/jobs/{jobId}/applications
Content-Type: application/json
Authorization: Bearer <token>

{
  "data": {
    "resume": "<glints-file-id>.pdf",
    "employerScreeningQuestionAnswers": [],
    "note": "",
    "attachments": []
  },
  "traceInfo": ""
}
```

The `resume` field contains the Glints-assigned file ID from CV upload (e.g., `61fbb36c71fe6d5daaa73db1c8f23d72.pdf`).

### 4. Get Hiring Questions (optional)

```
POST https://glints.com/api/v2-alc/graphql?op=getOneTapJobApplyQuestions
Authorization: Bearer <token>

{
  "operationName": "getOneTapJobApplyQuestions",
  "variables": { "jobId": "<job-uuid>" },
  "query": "query getOneTapJobApplyQuestions($jobId: String!) { getOneTapJobApplyQuestions(jobId: $jobId) { profileQuestions { name type __typename } __typename } }"
}
```

## Apply Flow (Step by Step)

The web apply form has 5 steps. Each must be completed before the next:

1. **Upload CV** (PDF) → Glints assigns a file ID
2. **Work Experience Duration** — radio: 0, <1yr, 1-3yr, 3-5yr, 5-10yr, 10+yr
3. **Skills Assessment** — per-skill radio: Tidak Berpengalaman / Dasar / Menengah / Ahli
4. **English Proficiency** — radio: Tidak Berpengalaman / Dasar / Menengah / Ahli / Fasih
5. **Notice Period** — radio: Segera, <1bulan, 1-3bulan, >3bulan
6. **Kirim** (Submit)

### Key UI Behavior

- **Not logged in:** LAMAR button → redirect to signup page
- **Logged in (desktop):** If `oneTapApply.isEligible = false` → shows "CHAT DENGAN HRD" (app-only). If eligible → shows "Lamar" ghost button.
- **Already applied:** Ghost button shows "Dilamar" (disabled) + message "Kamu sudah melamar pekerjaan ini."
- **Button selector:** `button.ghostbtn-content` with text "Lamar" (not "Dilamar")

## Scripts

### glints_scan.py — Job Scanner

Search Glints for jobs by keyword. Outputs structured JSON.

```bash
python3 scripts/glints_scan.py "legal associate"
```

### glints_auto_apply.py — Full Auto-Apply

Login → Search → Filter → Upload CV → Apply to all matching jobs.

```bash
python3 scripts/glints_auto_apply.py
```

Configuration (edit in script):
- `EMAIL` / `PASSWORD` — Glints credentials
- `CV_PATH` — path to CV PDF
- `KEYWORDS` — search terms
- Filters: city, salary minimum, experience level

## CloakBrowser Usage

```python
from cloakbrowser import launch

browser = launch(headless=True, humanize=True)
page = browser.new_page()

# Login with expect_response to capture token
page.goto('https://glints.com/id/login', timeout=30000)
time.sleep(8)
page.click('text="Masuk dengan Email"')
time.sleep(3)
page.fill('#login-form-email', '<email>')
page.fill('#login-form-password', '<password>')
time.sleep(0.5)

with page.expect_response(lambda r: 'oauth2/token' in r.url, timeout=15000) as ri:
    page.evaluate('() => document.querySelector("form").dispatchEvent(new Event("submit", {bubbles:true,cancelable:true}))')
token = json.loads(ri.value.text())['access_token']
```

### Key CloakBrowser Notes

- `humanize=True` — enables human-like mouse curves, typing delays, scroll patterns
- `page.evaluate()` for JS clicks (form submit), `page.click()` for human-like clicks
- `page.expect_response()` to capture specific HTTP responses
- `page.context.on('request'/'response')` for intercepting API calls
- Cloudflare bypass: automatic with CloakBrowser (58 C++ source patches)
- `headless=False` if bot detection still blocks (uses display)

## Common Pitfalls

1. **Using curl instead of CloakBrowser.** Cloudflare WAF blocks all non-browser requests to glints.com/api. Always use CloakBrowser.

2. **Trying to apply when `oneTapApply.isEligible = false`.** Some jobs only allow app-based applications. The web form won't open. Check the button state before clicking.

3. **Not checking `isApplied` before applying.** The API returns `isApplied: true` in search results. Filter these out to avoid wasted attempts.

4. **Clearing captured API calls before Kirim click.** The apply mutation fires on Kirim click. Set up capture BEFORE the click, not after.

5. **Using Python `and`/`or` in JavaScript evaluate().** Always use `&&`/`||` in page.evaluate() JS strings.

6. **Expecting GraphQL for apply.** The apply endpoint is REST (`/api/v2/v2/jobs/{jobId}/applications`), not GraphQL. Many devs assume GraphQL because search uses it.

7. **Token not persisting.** The Bearer token from OAuth2 login is session-based. Re-login if you get 401 errors.

8. **File input not appearing.** The LAMAR button must be clicked via CloakBrowser's human-like click (not JS `.click()`). Use `page.evaluate()` only for form submission.

## Verification Checklist

- [ ] CloakBrowser installed and binary downloaded
- [ ] Glints credentials available
- [ ] CV PDF prepared at specified path
- [ ] Login returns 200 with access_token
- [ ] Search returns job listings
- [ ] At least one job passes filters (city, salary, not applied)
- [ ] Apply returns "Applied: True" for test job
- [ ] Results saved to JSON for review
