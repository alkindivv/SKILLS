# JobStreet GraphQL Operations

Captured from live JobStreet sessions. Used for job search, details, and tracking.

## Endpoint

```
POST https://id.jobstreet.com/graphql
```

## JobCountsV6

Job search results with full metadata.

```graphql
query JobCountsV6($searchRequest: JobSearchRequest!) {
  jobCountsV6(searchRequest: $searchRequest) {
    totalCount
    classificationCounts {
      classification {
        id
        description
      }
      count
    }
    locationCounts {
      location {
        id
        description
      }
      count
    }
  }
}
```

**Variables:**
```json
{
  "searchRequest": {
    "keywords": "legal counsel",
    "location": "Jakarta",
    "pageSize": 20,
    "page": 1
  }
}
```

**Response size:** ~34KB

## jobDetailsPersonalised

Get personalized job details (requires auth).

```graphql
query jobDetailsPersonalised($jobId: String!) {
  jobDetailsPersonalised(jobId: $jobId) {
    jobId
    title
    company
    isApplied
    isSaved
  }
}
```

## TrackJobDetailsViewed

Track that a job was viewed (analytics).

```graphql
mutation TrackJobDetailsViewed($jobId: String!) {
  trackJobDetailsViewed(jobId: $jobId) {
    success
  }
}
```

## createCandidateJobMatchStrongFitRequest

Check if candidate is a strong fit.

```graphql
query createCandidateJobMatchStrongFitRequest($jobId: String!) {
  createCandidateJobMatchStrongFitRequest(jobId: $jobId) {
    isStrongFit
    matchScore
  }
}
```

## JobDetailsRecommendedJobs

Get recommended jobs based on current job.

```graphql
query JobDetailsRecommendedJobs($jobId: String!) {
  jobDetailsRecommendedJobs(jobId: $jobId) {
    jobs {
      id
      title
      company
    }
  }
}
```

## getJobDetailsBadges

Get badges for a job posting.

```graphql
query getJobDetailsBadges($jobId: String!) {
  getJobDetailsBadges(jobId: $jobId) {
    badges {
      type
      label
    }
  }
}
```

## GetBanner

Get banner content.

```graphql
query GetBanner {
  getBanner {
    title
    message
    link
  }
}
```

## Public REST API

No auth required for job search:

```bash
curl "https://id.jobstreet.com/api/jobsearch/v5/search?keywords=hukum&location=Jakarta&page=1&pageSize=20"
```

**Response:**
```json
{
  "totalCount": 661,
  "jobs": [
    {
      "id": "92535231",
      "title": "Legal Administration (Jabodetabek)",
      "advertiser": {
        "description": "PT Dipo Star Finance"
      },
      "workType": "Full Time",
      "location": "Jakarta"
    }
  ]
}
```

## Notes

- GraphQL introspection is blocked (returns 403)
- Some queries return empty data when not authenticated (72b, 73b responses)
- `JobCountsV6` works without auth and returns full results
- The `sol` parameter in URLs is a tracking hash, not required for API calls
