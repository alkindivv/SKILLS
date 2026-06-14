# Glints API Reference (Reverse-Engineered)

All endpoints require CloakBrowser for access (Cloudflare WAF blocks curl/standard headless).

## Authentication

### OAuth2 Login
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

**Response (200):**
```json
{
  "access_token": "eyJhbG...P1_U",
  "activeRole": "CANDIDATE",
  "availableRoles": ["CANDIDATE"],
  "token_type": "Bearer",
  "isAuthenticated": true
}
```

**Notes:**
- `client_id` is public (no secret needed)
- Token is session-based, expires after inactivity
- Use as `Authorization: Bearer <token>` in subsequent requests

## Job Search (GraphQL)

### searchJobsV3
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
  "query": "query searchJobsV3($data: JobSearchConditionInput!) { searchJobsV3(data: $data) { jobsInPage { id title company { name } city { name } salaries { minAmount maxAmount CurrencyCode } isApplied type educationLevel minYearsOfExperience maxYearsOfExperience workArrangementOption status } hasMore } }"
}
```

**Key fields in response:**
- `id` — UUID, used in apply endpoint
- `isApplied` — boolean, check before applying
- `salaries[0].minAmount` — 0 if not displayed
- `city.name` — null for Jakarta default

### getOneTapJobApplyQuestions
```
POST https://glints.com/api/v2-alc/graphql?op=getOneTapJobApplyQuestions
Authorization: Bearer <token>

{
  "operationName": "getOneTapJobApplyQuestions",
  "variables": { "jobId": "<uuid>" },
  "query": "query getOneTapJobApplyQuestions($jobId: String!) { getOneTapJobApplyQuestions(jobId: $jobId) { profileQuestions { name type __typename } __typename } }"
}
```

**Profile question types:** BIRTH_DATE, GENDER, LOCATION, MONTHLY_SALARY_EXPECTATION, PAST_JOB_ROLES, LATEST_EDUCATION_EXPERIENCE, RESUME

## Job Application (REST)

### Submit Application
```
POST https://glints.com/api/v2/v2/jobs/{jobId}/applications
Content-Type: application/json
Authorization: Bearer <token>

{
  "data": {
    "resume": "61fbb36c71fe6d5daaa73db1c8f23d72.pdf",
    "employerScreeningQuestionAnswers": [],
    "note": "",
    "attachments": []
  },
  "traceInfo": ""
}
```

**Important:** This is a REST endpoint, NOT GraphQL. The `resume` field contains the Glints-assigned filename from the CV upload step (via browser file input).

**Response (200):** Application submitted successfully. Check `isApplied: true` in subsequent search results.

## Introspection Notes

- GraphQL introspection is **blocked** for mutation types (returns only 6 employer-side mutations)
- The apply mutation is NOT GraphQL — it's REST
- Schema introspection for query types works partially with `variables: {}` (empty object required)
- The `OneTapJobApplyQuestions` type has field `profileQuestions` (not `questions`)
- `OneTapJobApplyProfileQuestion` does NOT have `required` field

## UI Behavior Matrix

| State | Button | Action |
|---|---|---|
| Not logged in | "Lamar" | Redirects to /signup |
| Logged in, not applied, eligible | "Lamar" ghost button | Opens apply form modal |
| Logged in, not applied, not eligible | "CHAT DENGAN HRD" | App-only apply |
| Logged in, already applied | "Dilamar" (disabled) | No action |
| oneTapApply.isEligible = true | "Lamar" | Web form |
| oneTapApply.isEligible = false | "CHAT DENGAN HRD" | Mobile app |

## CloakBrowser Detection Bypass

CloakBrowser passes all major bot detection tests:
- reCAPTCHA v3: 0.9 score (human-level)
- Cloudflare Turnstile: passed
- FingerprintJS: passed
- BrowserScan: 4/4 checks passed
- navigator.webdriver: false

Key options:
- `humanize=True` — human-like mouse/keyboard/scroll behavior
- `headless=True` — use headless mode (some sites need `False`)
- `proxy="http://..."` — residential proxy for aggressive sites
