---
name: kalibrr-auto-apply
description: "Use when searching or auto-applying to jobs on Kalibrr Indonesia. Reverse-engineered Kalibrr API — simple REST POST with static CSRF token + JWT cookie. Use whenever user mentions Kalibrr, job scanning, auto-apply, or wants to apply to Indonesian jobs programmatically."
version: 1.0.0
author: AL KINDI
license: MIT
metadata:
  hermes:
    tags: [kalibrr, jobs, auto-apply, indonesia, career, automation, api]
    related_skills: [jobstreet-auto-apply, glints-auto-apply, deep-research, legal-career-strategy]
---

# Kalibrr Auto-Apply

Automate job application on Kalibrr Indonesia via simple REST API — no browser automation needed for applying!

## Overview

Kalibrr uses a straightforward REST API with JWT authentication. The apply endpoint is a single `POST` request with a static CSRF token. No Cloudflare, no CAPTCHA, no multi-step forms.

**Key advantage:** Unlike JobStreet (Turnstile) and Glints (Cloudflare WAF), Kalibrr's apply API works directly via `curl` — no browser automation needed!

## When to Use

- User wants to apply to jobs on Kalibrr Indonesia
- User mentions "Kalibrr", "job scanning", "auto-apply"
- Career agent needs to mass-apply on Kalibrr

**Don't use for:**
- JobStreet jobs (use `jobstreet-auto-apply`)
- Glints jobs (use `glints-auto-apply`)

## Architecture

```
curl → POST /api/candidate/job_applications/{jobId}
         ↓
    Headers: KB-CSRF + Cookie: kb={JWT}
         ↓
    Body: {"app_source": "job-full-page"}
         ↓
    Response: 200 OK (application submitted)
```

## Authentication

### JWT Token (`kb` cookie)

- **Domain:** `jobseeker.kalibrr.com`
- **Cookie name:** `kb`
- **Format:** RS256 JWT
- **Contains:** user_id, email, first_name, last_name, country_code, roles, expiry_date
- **Expiry:** Server doesn't strictly enforce — works even after `expiry_date` passes

### CSRF Token

- **Header name:** `KB-CSRF`
- **Value:** Static token (doesn't change between requests)
- **Example:** `j.jH-DS9,evr7w%~dI/T!wmgH8u5Rxd.`
- **Source:** Embedded in JavaScript bundle (not in HTML or cookies)

### Getting the Token

1. **From browser cookies:** Export `kb` cookie from Chrome DevTools
2. **From agent-browser:** `agent-browser state save /tmp/kalibrr_state.json`

## API Endpoints

### Apply to Job (PRIMARY)

```
POST https://jobseeker.kalibrr.com/api/candidate/job_applications/{jobId}
```

**Headers:**
```
Content-Type: application/json
Accept: application/json, text/plain, */*
KB-CSRF: {static_csrf_token}
Cookie: kb={jwt_token}
```

**Body:**
```json
{"app_source": "job-full-page"}
```

**Response (200 OK):**
```json
{
  "status": 1,
  "state_category_id": 304,
  "job_id": 267376,
  "company_id": 26946,
  "user_id": 8814574,
  "verdict": "pending",
  "relevance_score": 0.0738,
  "created_at": "2026-06-14T22:07:07.761914+00:00"
}
```

**State categories:**
- `263` = Applied (incomplete profile)
- `304` = Applied (complete profile)

### Get Job Details

```
GET https://jobseeker.kalibrr.com/kjp/jobs/{jobId}?with_applied=true&with_exams=true&with_profilers=true
```

### Check Application Status

```
GET https://jobseeker.kalibrr.com/api/candidate/job_applications/{jobId}
```

### Get Candidate Profile

```
GET https://jobseeker.kalibrr.com/api/candidates/{candidateId}/profilers?types=PersonalInformationProfiler,WorkHistoryProfiler,EducationProfiler,FileUploadProfiler,SDSSkillProfiler,SalaryProfiler
```

## Search

Kalibrr search is **server-side rendered** — no API endpoint for job search. Use agent-browser to scrape job links from search pages:

```
https://jobseeker.kalibrr.com/job-board/te/{keyword}/1
```

**URL pattern:** `https://jobseeker.kalibrr.com/c/{company-slug}/jobs/{job-id}/{job-slug}`

## Usage

### Direct curl Apply

```bash
curl -X POST "https://jobseeker.kalibrr.com/api/candidate/job_applications/267376" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/plain, */*" \
  -H "KB-CSRF: j.jH-DS9,evr7w%~dI/T!wmgH8u5Rxd." \
  -H "Cookie: kb=eyJhbG...your_jwt_token" \
  -d '{"app_source":"job-full-page"}'
```

### Batch Apply Script

```bash
# Dry run
bash scripts/kalibrr_auto_apply.sh --search "legal counsel" --max 5 --dry-run

# Real apply
bash scripts/kalibrr_auto_apply.sh --search "legal counsel" --max 10
```

## Pitfalls

1. **JWT expiry** — Server doesn't strictly enforce, but very old tokens may fail. Re-export if 401 errors appear.

2. **CSRF token is static** — Don't need to refresh it. Same token works across sessions.

3. **Rate limiting** — No observed rate limiting, but add 2-second delays between applies to be safe.

4. **Already applied** — Returns 409 if already applied to a job. Script handles this gracefully.

5. **Search is SSR** — No API for job search. Must use browser to get job IDs from search results.

6. **Profile completion** — Some jobs require complete profile. `state_category_id: 263` = incomplete, `304` = complete.

## Files

| File | Description |
|------|-------------|
| `scripts/kalibrr_auto_apply.sh` | Main auto-apply script |
| `references/api_endpoints.md` | Full API endpoint reference |

## Successfully Applied

- Commercial Legal @ PT Murni Development Indonesia (job ID: 268278)
- Legal Officer @ OttoDigital Group (job ID: 267376)
- Legal Consultant Staff @ PT BREXA Raya Indonesia (job ID: 268390)
- Compliance Manager @ OttoDigital Group (job ID: 266168)
- Business Development @ Mamikos (job ID: 264609)
