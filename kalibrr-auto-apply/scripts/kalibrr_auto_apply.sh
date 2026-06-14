#!/bin/bash
# Kalibrr Auto-Apply Script
# Uses curl with static CSRF token + kb cookie
#
# Usage: bash kalibrr_auto_apply.sh [--search "legal counsel"] [--max 5] [--dry-run]

set -euo pipefail

# Config
KB_TOKEN_FILE="/tmp/kb_token.txt"
CSRF_TOKEN="j.jH-DS9,evr7w%~dI/T!wmgH8u5Rxd."
SEARCH_QUERY="${1:-legal counsel}"
MAX_APPLIES="${2:-10}"
DRY_RUN="${3:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Kalibrr Auto-Apply ===${NC}"
echo "Search: $SEARCH_QUERY"
echo "Max applies: $MAX_APPLIES"
echo "Dry run: ${DRY_RUN:-no}"
echo ""

# Check prerequisites
if [ ! -f "$KB_TOKEN_FILE" ]; then
  echo -e "${RED}❌ KB token not found. Save token to $KB_TOKEN_FILE${NC}"
  echo "  echo 'eyJhbG...' > $KB_TOKEN_FILE"
  exit 1
fi

KB_TOKEN=$(cat "$KB_TOKEN_FILE")
echo -e "${GREEN}✓ KB token loaded (${#KB_TOKEN} chars)${NC}"

# Function to apply to a job
apply_to_job() {
  local job_id="$1"
  local job_title="$2"
  
  echo -e "\n${YELLOW}Applying to: $job_title (ID: $job_id)${NC}"
  
  if [ "$DRY_RUN" = "--dry-run" ]; then
    echo -e "  ${YELLOW}[DRY RUN] Skipping actual apply${NC}"
    return 0
  fi
  
  response=$(curl -s -w "\n%{http_code}" -X POST \
    "https://jobseeker.kalibrr.com/api/candidate/job_applications/$job_id" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/plain, */*" \
    -H "KB-CSRF: $CSRF_TOKEN" \
    -H "Cookie: kb=$KB_TOKEN" \
    -d '{"app_source":"job-full-page"}')
  
  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')
  
  if [ "$http_code" = "200" ]; then
    state=$(echo "$body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('state_category_id', '?'))" 2>/dev/null || echo "?")
    echo -e "  ${GREEN}✅ Applied! state_category_id=$state${NC}"
    return 0
  elif [ "$http_code" = "401" ]; then
    echo -e "  ${RED}❌ Auth failed (401). Token expired?${NC}"
    return 1
  elif [ "$http_code" = "409" ]; then
    echo -e "  ${YELLOW}⚠️ Already applied (409)${NC}"
    return 0
  else
    echo -e "  ${RED}❌ Failed ($http_code): ${body:0:100}${NC}"
    return 1
  fi
}

# Function to get job IDs from search page (requires agent-browser)
get_jobs_from_browser() {
  export DISPLAY=:99
  
  echo -e "\n${YELLOW}Searching for jobs via browser...${NC}"
  
  # Open search page
  encoded_query=$(echo "$SEARCH_QUERY" | sed 's/ /%20/g')
  agent-browser open "https://jobseeker.kalibrr.com/job-board/te/${encoded_query}/1" 2>/dev/null
  sleep 5
  
  # Extract job links
  agent-browser eval "JSON.stringify([...document.querySelectorAll('a')].filter(a => {
    const href = a.href || '';
    const text = a.textContent?.trim() || '';
    return href.includes('/c/') && href.includes('/jobs/') && text.length > 5 && text.length < 100;
  }).map(a => {
    const match = a.href.match(/\/jobs\/(\d+)\//);
    return {
      id: match ? match[1] : null,
      title: a.textContent?.trim()?.substring(0, 60)
    };
  }).filter(j => j.id).reduce((acc, j) => {
    if (!acc.find(x => x.id === j.id)) acc.push(j);
    return acc;
  }, []).slice(0, $MAX_APPLIES))" 2>/dev/null
}

# Main
echo -e "\n${YELLOW}[1] Getting job listings...${NC}"
jobs_json=$(get_jobs_from_browser)

if [ -z "$jobs_json" ] || [ "$jobs_json" = "[]" ]; then
  echo -e "${RED}No jobs found${NC}"
  exit 1
fi

job_count=$(echo "$jobs_json" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
echo -e "${GREEN}Found $job_count jobs${NC}"

# Show jobs
echo "$jobs_json" | python3 -c "
import sys, json
jobs = json.load(sys.stdin)
for i, j in enumerate(jobs, 1):
    print(f\"  {i}. {j['title']} (ID: {j['id']})\"  )

# Apply to each job
echo -e "\n${YELLOW}[2] Applying to jobs...${NC}"
applied=0
failed=0

echo "$jobs_json" | python3 -c "
import sys, json
jobs = json.load(sys.stdin)
for j in jobs:
    print(f\"{j['id']}|{j['title']}\")
" | while IFS='|' read -r job_id job_title; do
  if apply_to_job "$job_id" "$job_title"; then
    applied=$((applied + 1))
  else
    failed=$((failed + 1))
  fi
  sleep 2  # Rate limiting
done

echo -e "\n${YELLOW}=== SUMMARY ===${NC}"
echo "Applied: $applied"
echo "Failed: $failed"
echo -e "\n${GREEN}Done!${NC}"
