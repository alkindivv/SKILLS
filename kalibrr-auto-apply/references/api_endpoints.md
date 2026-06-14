# Kalibrr API Endpoints Reference

Base URL: `https://jobseeker.kalibrr.com`

## Authentication

All endpoints require:
- `Cookie: kb={JWT_TOKEN}` — JWT authentication
- `KB-CSRF: {CSRF_TOKEN}` — CSRF protection (static token)

## Job Applications

### POST /api/candidate/job_applications/{jobId}

Apply to a job.

**Request:**
```http
POST /api/candidate/job_applications/267376 HTTP/1.1
Host: jobseeker.kalibrr.com
Content-Type: application/json
Accept: application/json, text/plain, */*
KB-CSRF: j.jH-DS9,evr7w%~dI/T!wmgH8u5Rxd.
Cookie: kb=eyJhbG...

{"app_source":"job-full-page"}
```

**Response (200 OK):**
```json
{
  "has_zapier_ats_integration": false,
  "relevance_score": 0.073865527287126,
  "reject_reapply": null,
  "updated_at": "2026-06-14T22:07:07.761914+00:00",
  "state_category_id": 304,
  "is_user_test": false,
  "user_id": 8814574,
  "job_id": 267376,
  "status": 1,
  "verdict": "pending",
  "company_id": 26946,
  "created_at": "2026-06-14T22:07:07.761914+00:00",
  "is_user_active": true,
  "is_user_verified": true
}
```

**Error responses:**
- `401` — Invalid/expired JWT or CSRF token
- `409` — Already applied to this job
- `422` — Invalid job ID

### GET /api/candidate/job_applications/{jobId}

Check application status.

**Response:**
```json
{
  "status": 1,
  "state_category_id": 304,
  "verdict": "pending",
  "seen": false,
  "date_application_completed": "2026-06-14T22:07:08.114731+00:00"
}
```

## Job Details

### GET /kjp/jobs/{jobId}

Get job details with profilers and application status.

**Query parameters:**
- `with_applied=true` — Include application status
- `with_exams=true` — Include exam requirements
- `with_profilers=true` — Include profiler requirements

**Response:** Full job object with company info, profilers, qualifications, etc.

## Candidate Profile

### GET /api/candidates/{candidateId}/profilers

Get candidate profile data.

**Query parameters:**
- `types` — Comma-separated profiler types

**Profiler types:**
- `PersonalInformationProfiler` — Name, phone, etc.
- `WorkHistoryProfiler` — Work experience
- `EducationProfiler` — Education history
- `FileUploadProfiler` — Resume file
- `SDSSkillProfiler` — Skills
- `SalaryProfiler` — Salary expectations
- `AboutMeProfiler` — Summary/bio
- `LanguageProfiler` — Language skills
- `LicenseProfiler` — Certifications

### GET /api/candidate/assessments

Get candidate assessment results.

## Search (Server-Side Rendered)

No API endpoint — search results are rendered server-side.

**Search URL:**
```
https://jobseeker.kalibrr.com/job-board/te/{keyword}/1
```

**Job URL pattern:**
```
https://jobseeker.kalibrr.com/c/{company-slug}/jobs/{job-id}/{job-slug}
```

## Job ID Extraction

From URL: `https://jobseeker.kalibrr.com/c/otto-digital/jobs/267376/legal-officer-3`
- Company slug: `otto-digital`
- Job ID: `267376`
- Job slug: `legal-officer-3`

Regex: `/\/jobs\/(\d+)\//`

## State Categories

| ID | Meaning |
|----|---------|
| 263 | Applied (incomplete profile) |
| 304 | Applied (complete profile) |

## Rate Limiting

No observed rate limiting. Recommended: 2-second delay between applies.

## Notes

- CSRF token is static — same value works across all requests
- JWT token works even after `expiry_date` in payload
- `app_source` field can be: `job-full-page`, `job-board`, `recommended`, etc.
- Response includes full job object — useful for logging/analytics
