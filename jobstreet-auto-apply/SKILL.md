---
name: jobstreet-auto-apply
description: "DEPRECATED — Use job-portal-auto-apply instead. This skill is kept for reference only."
version: 3.0.0
author: AL KINDI
license: MIT
metadata:
  hermes:
    tags: [jobstreet, jobs, auto-apply, indonesia, career, automation, graphql-api, cover-letter]
    related_skills: [job-portal-auto-apply, glints-auto-apply, deep-research, content-intelligence, legal-career-strategy]
---

# ⚠️ DEPRECATED — Use `job-portal-auto-apply` skill

This skill is **outdated**. The active skill is `job-portal-auto-apply` in the Hermes skill system.

## What Changed

| Old (this skill) | New (`job-portal-auto-apply`) |
|---|---|
| Browser-based apply (agent-browser + Xvfb) | **GraphQL API apply** (no browser needed) |
| 4-step form automation | Single API call per job |
| No cover letter support | **Cover letter: written + upload** |
| ~30 seconds per job | **~5 seconds per job** |
| v2.0.0 | **v3.0.0** |

## Quick Reference (v4 API)

```python
# Auth (needs BOTH token + cookies)
from jobstreet_api_v4 import JobStreetClient
from jobstreet_api_v3 import JobStreetAPI

v4 = JobStreetClient.from_token_file('/tmp/jobstreet_token.txt', '/tmp/jobstreet_auth_fresh.json')
v3 = JobStreetAPI.from_token_file('/tmp/jobstreet_token.txt')

# Generate cover letter
cl_uri = v4.write_cover_letter('Saya Al Kindi, S.H....')

# Apply
result = v3.apply_to_job(
    job_id='92413665',
    resume_id='ee375305-6212-4748-bba3-9375a1b0419f',
    most_recent_role={'company': 'RAF', 'title': 'Junior Associate', 'started': {'year': 2026, 'month': 2}},
    cover_letter_uri=cl_uri,
    cover_letter_text='Saya Al Kindi, S.H....',
)
```

## Token Capture (still needed)

```bash
export DISPLAY=:99
python3 /root/.hermes/profiles/career/capture_token.py
```

## Files

| File | Description |
|---|---|
| `/root/.hermes/profiles/career/jobstreet_api_v4.py` | API client v4 (apply + cover letter) |
| `/root/.hermes/profiles/career/jobstreet_api_v3.py` | API client v3 (apply only) |
| `/root/.hermes/profiles/career/capture_token.py` | Token capture script |

## See Also

- `job-portal-auto-apply` skill — full documentation with all portals
- `references/graphql_queries.md` — captured GraphQL operations (historical)
- `references/select_options.md` — question ID mappings (historical)
