#!/usr/bin/env python3
"""
Glints Legal Job Scanner — CloakBrowser + GraphQL
Searches for legal/law jobs on Glints Indonesia using stealth browser.
Bypasses Cloudflare WAF via CloakBrowser's 58 C++ source patches.

Usage:
    python3 glints_scan.py "legal associate"
    python3 glints_scan.py "corporate legal" --city Jakarta
"""

from cloakbrowser import launch
import time
import json
import sys

SEARCH_KEYWORDS = [
    "legal associate",
    "law firm",
    "hukum",
    "legal officer",
    "compliance",
    "paralegal",
    "corporate legal",
    "in-house counsel",
    "advokat",
]

def search_jobs(page, keyword, location="Jakarta"):
    """Search Glints for jobs via GraphQL searchJobsV3.
    
    Intercepts the GraphQL response from Glints' frontend SPA
    rather than making direct API calls (which are blocked by Cloudflare).
    """
    jobs_found = []
    
    def handle_response(response):
        if 'graphql' in response.url and 'searchJobsV3' in response.url:
            try:
                data = response.json()
                jobs = data.get('data', {}).get('searchJobsV3', {}).get('jobsInPage', [])
                jobs_found.extend(jobs)
            except:
                pass
    
    page.on('response', handle_response)
    
    url = f'https://glints.com/id/opportunities/jobs/explore?country=ID&keyword={keyword.replace(" ", "+")}&locationName={location}'
    page.goto(url, timeout=30000)
    time.sleep(6)
    
    page.remove_listener('response', handle_response)
    return jobs_found

def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "legal associate"
    location = "Jakarta"
    
    # Parse --city flag
    for i, arg in enumerate(sys.argv):
        if arg == "--city" and i + 1 < len(sys.argv):
            location = sys.argv[i + 1]
    
    print(f"Searching Glints for: {keyword} in {location}")
    print("=" * 60)
    
    browser = launch(headless=True, humanize=True)
    page = browser.new_page()
    
    jobs = search_jobs(page, keyword, location)
    
    # Deduplicate by job ID
    seen = set()
    unique_jobs = []
    for job in jobs:
        jid = job.get('id')
        if jid and jid not in seen:
            seen.add(jid)
            unique_jobs.append(job)
    
    print(f"\nFound {len(unique_jobs)} unique jobs\n")
    
    for i, job in enumerate(unique_jobs):
        title = job.get('title', 'N/A')
        company = job.get('company', {}).get('name', 'N/A')
        city_data = job.get('city')
        city = city_data.get('name', '') if city_data else ''
        salary_data = job.get('salaries', [])
        salary = ''
        if salary_data:
            s = salary_data[0]
            min_amt = s.get('minAmount', 0)
            max_amt = s.get('maxAmount', 0)
            currency = s.get('CurrencyCode', 'IDR')
            if min_amt and max_amt:
                salary = f"{currency} {min_amt:,.0f} - {max_amt:,.0f}"
        job_type = job.get('type', 'N/A')
        exp_min = job.get('minYearsOfExperience', 0)
        exp_max = job.get('maxYearsOfExperience', 0)
        education = job.get('educationLevel', 'N/A')
        is_applied = job.get('isApplied', False)
        job_id = job.get('id')
        work_arrangement = job.get('workArrangementOption', '')
        
        location_str = city or 'Jakarta'
        salary_str = salary or 'Gaji Tidak Ditampilkan'
        exp_str = f"{exp_min}-{exp_max} tahun" if exp_max else f"{exp_min}+ tahun"
        applied_str = " [APPLIED]" if is_applied else ""
        
        print(f"  {i+1}. {title}")
        print(f"     Company: {company}")
        print(f"     Location: {location_str} | Salary: {salary_str}")
        print(f"     Type: {job_type} | Edu: {education} | Exp: {exp_str}")
        print(f"     Mode: {work_arrangement}{applied_str}")
        print(f"     URL: https://glints.com/id/opportunities/jobs/{job_id}")
        print()
    
    # Save to JSON
    output = {
        'keyword': keyword,
        'location': location,
        'total': len(unique_jobs),
        'jobs': [{
            'id': j.get('id'),
            'title': j.get('title'),
            'company': j.get('company', {}).get('name'),
            'city': j.get('city', {}).get('name') if j.get('city') else None,
            'type': j.get('type'),
            'education': j.get('educationLevel'),
            'salary': j.get('salaries'),
            'is_applied': j.get('isApplied'),
            'work_arrangement': j.get('workArrangementOption'),
            'url': f"https://glints.com/id/opportunities/jobs/{j.get('id')}"
        } for j in unique_jobs]
    }
    
    output_path = '/tmp/glints_scan.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Saved to {output_path}")
    
    browser.close()

if __name__ == '__main__':
    main()
