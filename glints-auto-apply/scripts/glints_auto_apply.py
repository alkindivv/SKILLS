#!/usr/bin/env python3
"""
Glints Auto-Apply — Full Automation Pipeline
Login → Search → Filter → Upload CV → Apply to all matching jobs.

Uses CloakBrowser (stealth Chromium) to bypass Cloudflare WAF.
Apply endpoint is REST (NOT GraphQL): POST /api/v2/v2/jobs/{jobId}/applications

Usage:
    python3 glints_auto_apply.py                    # Run with defaults
    python3 glints_auto_apply.py --dry-run          # Search only, don't apply
    python3 glints_auto_apply.py --keyword "hukum"  # Custom keyword
"""

from cloakbrowser import launch
import time
import json
import sys
import os

# ============================================================
# CONFIGURATION — Edit these before running
# ============================================================
EMAIL = os.environ.get('GLINTS_EMAIL', 'witcave@gmail.com')
PASSWORD = os.environ.get('GLINTS_PASSWORD', 'Batam123')
CV_PATH = os.environ.get('GLINTS_CV', '/root/.hermes/profiles/career/workspace/career-ops/output/cv-al-kindi-final-2026-06-11.pdf')
OUTPUT_PATH = '/tmp/glints_apply_results.json'

KEYWORDS = [
    "legal associate",
    "law firm",
    "hukum",
    "legal officer",
    "compliance",
    "corporate legal",
    "advokat",
]

# Filters
MIN_SALARY = 4_000_000  # IDR
CITY_FILTER = "jakarta"  # substring match (case-insensitive)
# ============================================================


def login(page):
    """Login via OAuth2 password grant and return Bearer token.
    
    Uses page.expect_response() to capture the OAuth2 token response
    from the form submission (not direct API call — Cloudflare blocks that).
    """
    page.goto('https://glints.com/id/login', timeout=30000)
    time.sleep(8)
    page.click('text="Masuk dengan Email"')
    time.sleep(3)
    page.fill('#login-form-email', EMAIL)
    page.fill('#login-form-password', PASSWORD)
    time.sleep(0.5)
    
    with page.expect_response(lambda r: 'oauth2/token' in r.url, timeout=15000) as ri:
        page.evaluate(
            '() => document.querySelector("form")'
            '.dispatchEvent(new Event("submit", {bubbles:true,cancelable:true}))'
        )
    data = json.loads(ri.value.text())
    token = data['access_token']
    time.sleep(5)
    return token


def search_jobs(page, keyword, location="Jakarta"):
    """Search Glints via intercepted GraphQL response.
    
    Navigates to the search page and captures the searchJobsV3
    GraphQL response from the SPA's network requests.
    """
    jobs_found = []
    
    def on_resp(response):
        if 'graphql' in response.url and 'searchJobsV3' in response.url:
            try:
                data = response.json()
                jobs = data.get('data', {}).get('searchJobsV3', {}).get('jobsInPage', [])
                jobs_found.extend(jobs)
            except:
                pass
    
    page.on('response', on_resp)
    url = f'https://glints.com/id/opportunities/jobs/explore?country=ID&keyword={keyword.replace(" ", "+")}&locationName={location}'
    page.goto(url, timeout=30000)
    time.sleep(6)
    page.remove_listener('response', on_resp)
    
    # Deduplicate
    seen = set()
    unique = []
    for j in jobs_found:
        jid = j.get('id')
        if jid and jid not in seen:
            seen.add(jid)
            unique.append(j)
    return unique


def upload_cv(page, cv_path):
    """Upload CV via the apply modal file input.
    
    The file input appears after clicking the "Lamar" ghost button.
    Returns True if upload succeeded, False if form didn't open.
    """
    # Click Lamar ghost button (must use JS click for ghost buttons)
    page.evaluate('''() => {
        document.querySelectorAll('button.ghostbtn-content').forEach(b => {
            if (b.textContent.trim() === 'Lamar' && !b.disabled) b.click()
        })
    }''')
    time.sleep(5)
    
    fi = page.query_selector('input[type="file"]')
    if not fi:
        return False
    
    fi.set_input_files(cv_path)
    time.sleep(3)
    return True


def fill_form_steps(page, steps=5):
    """Fill all radio-button steps in the apply form.
    
    For each step: click "Selanjutnya" (Next), then select the
    first available radio option in each unanswered group.
    """
    for step in range(steps):
        # Click Selanjutnya
        page.evaluate('''() => {
            document.querySelectorAll('button').forEach(b => {
                if (b.textContent.trim() === 'Selanjutnya' && b.offsetParent) b.click()
            })
        }''')
        time.sleep(2)
        
        # Fill all unanswered radio groups
        page.evaluate('''() => {
            const groups = new Set()
            document.querySelectorAll('input[type="radio"]:not(:checked)')
                .forEach(r => groups.add(r.getAttribute('name')))
            groups.forEach(name => {
                const rs = document.querySelectorAll('input[name="' + name + '"]')
                if (!Array.from(rs).some(x => x.checked)) {
                    if (rs.length >= 3) rs[2].click()       // "Menengah" / 1-3yr
                    else if (rs.length >= 2) rs[1].click()   // Second option
                }
            })
        }''')
        time.sleep(1)


def apply_to_job(page, job_id, cv_path):
    """Apply to a single job. Returns dict with status and details.
    
    Flow: navigate → check status → upload CV → fill form → submit
    The actual API call is:
        POST /api/v2/v2/jobs/{jobId}/applications
        Body: {"data":{"resume":"fileId.pdf","employerScreeningQuestionAnswers":[],"note":"","attachments":[]},"traceInfo":""}
    """
    # Navigate to job page (use /x/ path which works for all jobs)
    job_url = f'https://glints.com/id/opportunities/jobs/x/{job_id}'
    page.goto(job_url, timeout=30000)
    time.sleep(8)
    
    # Check if already applied
    already = page.evaluate('() => document.body.innerText.includes("sudah melamar")')
    if already:
        return {'status': 'already_applied'}
    
    # Upload CV (opens form modal)
    uploaded = upload_cv(page, cv_path)
    if not uploaded:
        return {'status': 'form_not_opened'}
    
    # Fill all form steps
    fill_form_steps(page, steps=5)
    
    # Capture the apply API response
    apply_result = None
    def on_resp(response):
        nonlocal apply_result
        if 'applications' in response.url and response.request.method == 'POST':
            try:
                apply_result = {
                    'status': response.status,
                    'body': response.text()[:2000]
                }
            except:
                pass
    page.context.on('response', on_resp)
    
    # Click Kirim (Submit)
    page.evaluate('''() => {
        document.querySelectorAll('button').forEach(b => {
            if (b.textContent.trim() === 'Kirim' && b.offsetParent) b.click()
        })
    }''')
    time.sleep(10)
    page.context.remove_listener('response', on_resp)
    
    # Verify result
    applied = page.evaluate(
        '() => document.body.innerText.includes("sudah melamar")'
        ' || document.body.innerText.includes("Berhasil")'
    )
    
    return {
        'status': 'applied' if applied else 'failed',
        'api_result': apply_result
    }


def filter_jobs(jobs):
    """Filter jobs by city, salary, and application status."""
    candidates = []
    for j in jobs:
        title = j.get('title', '')
        company = j.get('company', {}).get('name', '')
        city = j.get('city', {})
        city_name = city.get('name', '') if city else ''
        is_applied = j.get('isApplied', False)
        salaries = j.get('salaries', [])
        min_salary = salaries[0].get('minAmount', 0) if salaries else 0
        
        # Skip if already applied
        if is_applied:
            continue
        
        # City filter (empty city = Jakarta default on Glints)
        if city_name and CITY_FILTER not in city_name.lower():
            continue
        
        # Salary filter (0 = not displayed, always include)
        if min_salary > 0 and min_salary < MIN_SALARY:
            continue
        
        candidates.append({
            'id': j.get('id'),
            'title': title,
            'company': company,
            'city': city_name or 'Jakarta',
            'salary': min_salary,
        })
    
    return candidates


def main():
    dry_run = '--dry-run' in sys.argv
    custom_kw = None
    for i, arg in enumerate(sys.argv):
        if arg == '--keyword' and i + 1 < len(sys.argv):
            custom_kw = sys.argv[i + 1]
    
    keywords = [custom_kw] if custom_kw else KEYWORDS
    
    print("=" * 60)
    print("Glints Auto-Apply")
    print("=" * 60)
    if dry_run:
        print("[DRY RUN] Will search but not apply")
    print(f"Email: {EMAIL}")
    print(f"CV: {CV_PATH}")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Filters: city={CITY_FILTER}, min_salary=Rp {MIN_SALARY:,}")
    print()
    
    browser = launch(headless=True, humanize=True)
    page = browser.new_page()
    
    # Step 1: Login
    print("[1/4] Logging in...")
    token = login(page)
    print(f"  Token: {token[:30]}...")
    
    # Step 2: Search all keywords
    print(f"\n[2/4] Searching {len(keywords)} keywords...")
    all_jobs = {}
    for kw in keywords:
        jobs = search_jobs(page, kw)
        for j in jobs:
            jid = j.get('id')
            if jid:
                all_jobs[jid] = j
        print(f'  "{kw}": {len(jobs)} results')
    print(f"  Total unique: {len(all_jobs)}")
    
    # Step 3: Filter
    print(f"\n[3/4] Filtering...")
    candidates = filter_jobs(list(all_jobs.values()))
    print(f"  Candidates: {len(candidates)}")
    for c in candidates:
        sal = f'Rp {c["salary"]:,.0f}' if c['salary'] > 0 else 'N/A'
        print(f"    {c['title']} - {c['company']} ({c['city']}) {sal}")
    
    if not candidates:
        print("\nNo matching jobs found. Try different keywords or filters.")
        browser.close()
        return
    
    if dry_run:
        print(f"\n[DRY RUN] Would apply to {len(candidates)} jobs. Exiting.")
        browser.close()
        return
    
    # Step 4: Apply
    print(f"\n[4/4] Applying to {len(candidates)} jobs...")
    results = []
    for i, c in enumerate(candidates):
        print(f"\n  [{i+1}/{len(candidates)}] {c['title']} - {c['company']}...")
        result = apply_to_job(page, c['id'], CV_PATH)
        result['job'] = c
        results.append(result)
        print(f"    -> {result['status']}")
        time.sleep(2)  # Rate limit
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    applied = sum(1 for r in results if r['status'] == 'applied')
    already = sum(1 for r in results if r['status'] == 'already_applied')
    failed = sum(1 for r in results if r['status'] not in ('applied', 'already_applied'))
    print(f"Applied: {applied}")
    print(f"Already applied: {already}")
    print(f"Failed: {failed}")
    print()
    
    for r in results:
        j = r['job']
        print(f"  [{r['status']}] {j['title']} - {j['company']}")
    
    # Save results
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {OUTPUT_PATH}")
    
    browser.close()


if __name__ == '__main__':
    main()
