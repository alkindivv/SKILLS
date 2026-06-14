---
name: jobstreet-auto-apply
description: "Use when searching or auto-applying to jobs on JobStreet Indonesia. Reverse-engineered JobStreet auth (SEEK Auth0 + Cloudflare Turnstile) and 4-step apply flow via agent-browser + Xvfb. Use whenever user mentions JobStreet, job scanning, auto-apply, or wants to apply to Indonesian jobs programmatically."
version: 2.0.0
author: AL KINDI
license: MIT
metadata:
  hermes:
    tags: [jobstreet, jobs, auto-apply, indonesia, career, automation, agent-browser, turnstile]
    related_skills: [glints-auto-apply, deep-research, content-intelligence, legal-career-strategy]
---

# JobStreet Auto-Apply

Automate job search and application on JobStreet Indonesia via agent-browser (Rust CLI) + Xvfb for Cloudflare Turnstile bypass.

## Overview

JobStreet Indonesia uses SEEK Auth0 with **Cloudflare Turnstile** (NOT Google reCAPTCHA) for bot protection. The error message misleadingly says "Please complete the recaptcha" but the actual widget is Turnstile.

**Critical discovery:** Turnstile ONLY auto-solves in **headed mode** with a display server (Xvfb). Headless mode fails silently — the widget renders but never completes.

The apply flow is a 4-step multi-page form: Resume → Role Requirements → Profile → Review & Submit.

## When to Use

- User wants to search legal/professional jobs on JobStreet Indonesia
- User wants to auto-apply to multiple JobStreet jobs
- User mentions "JobStreet", "job scanning", "auto-apply"
- Career agent needs to scan Indonesian job portals
- User provides JobStreet cookies for authentication

**Don't use for:**
- Glints jobs (use `glints-auto-apply` skill instead)
- International job platforms (LinkedIn, Indeed)
- Job portals that don't use SEEK Auth0

## Architecture

```
User → agent-browser (Rust CLI) → Chromium (headed + Xvfb) → JobStreet
                                    ↑
                          Turnstile auto-solves in headed mode
```

## Prerequisites

```bash
# Install agent-browser
npm install -g agent-browser
agent-browser install

# Install Xvfb (Linux display server)
apt install xvfb

# Verify installation
agent-browser --version  # v0.27.3+
which Xvfb
```

## Authentication Flow

### First-Time Login (Manual)

1. Start Xvfb:
   ```bash
   Xvfb :99 -screen 0 1920x1080x24 &
   export DISPLAY=:99
   ```

2. Open JobStreet login:
   ```bash
   agent-browser --headed open https://id.jobstreet.com/oauth/login
   ```

3. Fill email and submit:
   ```bash
   agent-browser fill @eN "email@gmail.com"
   agent-browser click @eM  # "Email me a sign in code" button
   ```

4. Wait for Turnstile to auto-solve (5-10 seconds)

5. Code input appears — enter 6-digit code from email:
   ```bash
   agent-browser fill @eK "123456"
   ```

6. Save auth state:
   ```bash
   agent-browser state save /tmp/jobstreet_auth.json
   ```

### Re-Using Auth State

```bash
agent-browser --headed --state /tmp/jobstreet_auth.json open https://id.jobstreet.com/
```

**Note:** Auth state expires after ~24 hours. Re-login if "Sign In" page appears.

## Search URL Pattern

```
https://id.jobstreet.com/{keyword}-jobs/in-{location}
https://id.jobstreet.com/legal-counsel-jobs/in-Jakarta
https://id.jobstreet.com/hukum-jobs/in-Jakarta
```

Public search API (no auth needed):
```
GET https://id.jobstreet.com/api/jobsearch/v5/search?keywords=hukum&location=Jakarta&page=1&pageSize=20
```

## Apply Flow (4 Steps)

### Step 1: Resume & Cover Letter

- URL: `https://id.jobstreet.com/id/job/{jobId}/apply`
- Upload CV:
  ```bash
  agent-browser upload '#resume-fileFile' /path/to/cv.pdf
  ```
- Select cover letter option (skip or upload):
  ```javascript
  agent-browser eval "(function(){
    var r = document.querySelectorAll('input[name=\"coverLetter-method\"]');
    for (var i=0; i<r.length; i++) { if (r[i].value === 'none') { r[i].click(); break; } }
    return 'done';
  })()"
  ```
- Click "Lanjut" button (use JS eval, not agent-browser click)

### Step 2: Role Requirements

- URL: `/apply/role-requirements`
- **Salary select:** `select[name*="2588"]` — options: "Rp 1 million" to "Rp 100 million or more"
- **Legal experience:** `select[name*="9ABA"]` — "No experience" to "More than 5 years"
- **Corporate law experience:** `select[name*="124"]` — same options
- **Languages:** checkboxes for English, Bahasa Indonesia, Mandarin, etc.
- **Proficiency:** checkboxes for "Speaks proficiently", "Writes proficiently", "Limited proficiency"
- **Notice period:** radio buttons — "None, I'm ready to go now", "Less than 1 month", etc.

Fill all fields via JS eval, then click "Lanjut".

### Step 3: Profile

- URL: `/apply/profile`
- Career history, education, licenses, skills auto-populated from Jobstreet profile
- Just click "Lanjut"

### Step 4: Review & Submit

- URL: `/apply/review`
- Check T&C checkbox
- Click "Kirim lamaran" (Submit application)
- Success URL: `/apply/success`
- Success text: "Lamaranmu telah dikirim ke {company}"

## Button Clicking Pattern

JobStreet React buttons need JS eval click (not agent-browser click):

```javascript
agent-browser eval "(function(){
  var btn = document.querySelectorAll('button');
  for (var i=0; i<btn.length; i++) {
    if (btn[i].textContent.includes('Lanjut')) {
      btn[i].scrollIntoView({block: 'center'});
      btn[i].click();
      return 'clicked';
    }
  }
  return 'not_found';
})()"
```

## Key CSS Selectors

| Element | Selector |
|---------|----------|
| Resume file input | `#resume-fileFile` |
| Cover letter file input | `#coverLetter-fileFile` |
| Salary select | `select[name*="2588"]` |
| Legal experience select | `select[name*="9ABA"]` |
| Corporate law select | `select[name*="124"]` |
| Language checkboxes | `input[name*="180"]` |
| Proficiency checkboxes | `input[name*="119"]` |
| Notice period radios | `input[name*="385"]` |
| T&C checkbox | `input[type=checkbox]` |

## Common Pitfalls

1. **Headless mode fails** — Turnstile doesn't render/auto-solve. Must use `--headed` + Xvfb.

2. **Button text has special chars** — "Lanjut⁠" (with invisible Unicode char). Use `includes()` not `===`.

3. **Radio buttons React-controlled** — Need direct `.click()` on input element, not label click.

4. **File upload** — Use CSS selector `#resume-fileFile`, not agent-browser ref. The `@eN` ref points to the button, not the file input.

5. **Auth state expires** — Session cookies expire after ~24h. Re-login if "Sign In" page appears.

6. **Xvfb cleanup** — Kill with `pkill -f Xvfb` after done to free resources.

7. **Select option IDs** — JobStreet uses cryptic option IDs (e.g., `ID_Q_2588_V_2_A_2600`). Map by iterating `select.options` and matching `.textContent`.

8. **Variable scope in eval** — Multiple `agent-browser eval` calls share the same page context. Use IIFE `(function(){...})()` to avoid `Identifier already declared` errors.

## Files

| File | Description |
|------|-------------|
| `scripts/jobstreet_auto_apply.js` | Main auto-apply script |
| `references/select_options.md` | Full select option ID mappings |
| `references/graphql_queries.md` | Captured GraphQL operations |

## Successfully Applied

- Legal Counsel @ PT YOFC International Indonesia (job ID: 92536575)
