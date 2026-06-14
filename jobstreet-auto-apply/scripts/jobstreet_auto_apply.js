#!/usr/bin/env node
/**
 * JobStreet Auto-Apply Script
 * Uses agent-browser (Rust CLI) with headed mode + Xvfb
 * 
 * Prerequisites:
 *   npm install -g agent-browser
 *   agent-browser install
 *   apt install xvfb
 * 
 * Auth state: /tmp/jobstreet_auth.json (saved from manual login)
 * 
 * Usage:
 *   node jobstreet_auto_apply.js [--search "legal counsel"] [--location "Jakarta"] [--max 5] [--dry-run]
 */

const { execSync } = require('child_process');
const fs = require('fs');

// Config
const AUTH_STATE = '/tmp/jobstreet_auth_final.json';
const CV_PATH = '/root/.hermes/profiles/career/workspace/career-ops/output/cv-al-kindi-final-2026-06-11.pdf';
const SEARCH_DEFAULT = 'legal counsel';
const LOCATION_DEFAULT = 'Jakarta';
const MAX_APPLIES_DEFAULT = 10;

// Parse args
const args = process.argv.slice(2);
const searchIdx = args.indexOf('--search');
const locationIdx = args.indexOf('--location');
const maxIdx = args.indexOf('--max');
const dryRun = args.includes('--dry-run');

const search = searchIdx >= 0 ? args[searchIdx + 1] : SEARCH_DEFAULT;
const location = locationIdx >= 0 ? args[locationIdx + 1] : LOCATION_DEFAULT;
const maxApplies = maxIdx >= 0 ? parseInt(args[maxIdx + 1]) : MAX_APPLIES_DEFAULT;

function run(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', timeout: 30000, env: { ...process.env, DISPLAY: ':99' } }).trim();
  } catch (e) {
    return e.stdout?.trim() || e.stderr?.trim() || 'ERROR';
  }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  console.log('=== JobStreet Auto-Apply ===');
  console.log(`Search: ${search}`);
  console.log(`Location: ${location}`);
  console.log(`Max applies: ${maxApplies}`);
  console.log(`Dry run: ${dryRun}`);
  console.log(`Auth state: ${AUTH_STATE}`);
  console.log('');

  // Check prerequisites
  if (!fs.existsSync(AUTH_STATE)) {
    console.error('❌ Auth state not found. Login first with agent-browser.');
    process.exit(1);
  }
  if (!fs.existsSync(CV_PATH)) {
    console.error('❌ CV not found at:', CV_PATH);
    process.exit(1);
  }

  // Start Xvfb
  console.log('[1] Starting Xvfb...');
  try { execSync('pkill -f Xvfb 2>/dev/null'); } catch (e) {}
  const xvfb = require('child_process').spawn('Xvfb', [':99', '-screen', '0', '1920x1080x24'], { 
    stdio: 'ignore', detached: true 
  });
  xvfb.unref();
  await sleep(2000);

  // Open JobStreet with auth state
  console.log('[2] Opening JobStreet...');
  run(`agent-browser --headed --state ${AUTH_STATE} open https://id.jobstreet.com/`);
  await sleep(3000);

  // Check if logged in
  const title = run('agent-browser eval "document.title"');
  console.log('[2] Title:', title);
  if (title.includes('Sign In') || title.includes('Candidate')) {
    console.error('❌ Not logged in. Re-login required.');
    process.exit(1);
  }

  // Search for jobs
  console.log('[3] Searching for jobs...');
  const searchUrl = `https://id.jobstreet.com/${encodeURIComponent(search)}-jobs/in-${encodeURIComponent(location)}`;
  run(`agent-browser open "${searchUrl}"`);
  await sleep(5000);

  // Get job links
  console.log('[4] Getting job links...');
  const jobLinksJson = run(`agent-browser eval "JSON.stringify([...document.querySelectorAll('a[href*='/job/']')].map(a => ({href: a.href, text: a.textContent.trim()})).filter(j => j.text && !j.text.includes('Lihat')).slice(0, ${maxApplies}))"`);
  
  let jobLinks;
  try {
    jobLinks = JSON.parse(jobLinksJson);
  } catch (e) {
    console.error('❌ Failed to parse job links:', jobLinksJson.substring(0, 200));
    process.exit(1);
  }

  console.log(`[4] Found ${jobLinks.length} jobs`);
  jobLinks.forEach((j, i) => console.log(`  ${i + 1}. ${j.text} - ${j.href?.substring(0, 60)}`));

  // Apply to each job
  let applied = 0;
  let failed = 0;
  const results = [];

  for (let i = 0; i < jobLinks.length; i++) {
    const job = jobLinks[i];
    console.log(`\n[${i + 5}] Applying to: ${job.text}`);
    
    if (dryRun) {
      console.log('  [DRY RUN] Skipping actual apply');
      results.push({ job: job.text, status: 'dry_run' });
      continue;
    }

    try {
      // Navigate to job page
      run(`agent-browser open "${job.href}"`);
      await sleep(3000);

      // Find and click apply button
      const applyClicked = run(`agent-browser eval "(function(){
        var links = document.querySelectorAll('a');
        for (var i=0; i<links.length; i++) {
          if (links[i].textContent.includes('Kirim lamaran') || links[i].href?.includes('/apply')) {
            links[i].click();
            return 'clicked';
          }
        }
        return 'not_found';
      })()"`);
      
      if (applyClicked === 'not_found') {
        console.log('  ⚠️ No apply button found (might be Easy Apply only)');
        results.push({ job: job.text, status: 'no_apply_button' });
        failed++;
        continue;
      }

      await sleep(5000);

      // STEP 1: Upload resume
      console.log('  [1/4] Uploading resume...');
      run(`agent-browser upload '#resume-fileFile' '${CV_PATH}'`);
      await sleep(3000);

      // Select "Jangan sertakan surat lamaran"
      run(`agent-browser eval "(function(){
        var r = document.querySelectorAll('input[name=\\"coverLetter-method\\"]');
        for (var i=0; i<r.length; i++) { if (r[i].value === 'none') { r[i].click(); break; } }
        return 'done';
      })()"`);
      await sleep(1000);

      // Click Lanjut
      run(`agent-browser eval "(function(){
        var btn = document.querySelectorAll('button');
        for (var i=0; i<btn.length; i++) {
          if (btn[i].textContent.includes('Lanjut')) { btn[i].click(); return 'clicked'; }
        }
        return 'not_found';
      })()"`);
      await sleep(8000);

      // STEP 2: Fill role requirements
      console.log('  [2/4] Filling role requirements...');
      const currentUrl = run('agent-browser eval "location.href"');
      
      if (currentUrl.includes('role-requirements')) {
        // Fill salary, experience, languages, notice
        run(`agent-browser eval "(function(){
          var selects = document.querySelectorAll('select');
          for (var i=0; i<selects.length; i++) {
            var opts = selects[i].options;
            if (opts.length > 5 && opts[1]?.text.includes('Rp')) {
              // Salary - select Rp 5-7 million range
              for (var j=0; j<opts.length; j++) {
                if (opts[j].text.includes('Rp 5 million') || opts[j].text.includes('Rp 7 million')) {
                  selects[i].value = opts[j].value;
                  selects[i].dispatchEvent(new Event('change', {bubbles: true}));
                  break;
                }
              }
            } else if (opts.length <= 10 && opts[1]?.text.includes('year')) {
              // Experience - select 1 year or Less than 1 year
              for (var j=0; j<opts.length; j++) {
                if (opts[j].text === '1 year' || opts[j].text === 'Less than 1 year') {
                  selects[i].value = opts[j].value;
                  selects[i].dispatchEvent(new Event('change', {bubbles: true}));
                  break;
                }
              }
            }
          }
          // Check languages
          var langCbs = document.querySelectorAll('input[type=checkbox]');
          for (var i=0; i<langCbs.length; i++) {
            var label = langCbs[i].labels?.[0]?.textContent || '';
            if (label.includes('English') || label.includes('Bahasa Indonesia') || 
                label.includes('Speaks proficiently') || label.includes('Writes proficiently')) {
              if (!langCbs[i].checked) langCbs[i].click();
            }
          }
          // Select notice period
          var noticeRadios = document.querySelectorAll('input[type=radio]');
          for (var i=0; i<noticeRadios.length; i++) {
            if (noticeRadios[i].labels?.[0]?.textContent?.includes('ready to go') || 
                noticeRadios[i].labels?.[0]?.textContent?.includes('None')) {
              noticeRadios[i].click();
              break;
            }
          }
          return 'filled';
        })()"`);
        await sleep(1000);

        // Click Lanjut
        run(`agent-browser eval "(function(){
          var btn = document.querySelectorAll('button');
          for (var i=0; i<btn.length; i++) {
            if (btn[i].textContent.includes('Lanjut')) { btn[i].click(); return 'clicked'; }
          }
          return 'not_found';
        })()"`);
        await sleep(8000);
      }

      // STEP 3: Profile (just click Lanjut)
      console.log('  [3/4] Profile step...');
      run(`agent-browser eval "(function(){
        var btn = document.querySelectorAll('button');
        for (var i=0; i<btn.length; i++) {
          if (btn[i].textContent.includes('Lanjut')) { btn[i].click(); return 'clicked'; }
        }
        return 'not_found';
      })()"`);
      await sleep(8000);

      // STEP 4: Review and submit
      console.log('  [4/4] Reviewing and submitting...');
      const reviewUrl = run('agent-browser eval "location.href"');
      
      if (reviewUrl.includes('review')) {
        // Check T&C checkbox
        run(`agent-browser eval "(function(){
          var cb = document.querySelector('input[type=checkbox]');
          if (cb && !cb.checked) cb.click();
          return 'checked';
        })()"`);
        await sleep(1000);

        // Click Kirim lamaran
        run(`agent-browser eval "(function(){
          var btn = document.querySelectorAll('button');
          for (var i=0; i<btn.length; i++) {
            if (btn[i].textContent.includes('Kirim lamaran')) { btn[i].click(); return 'clicked'; }
          }
          return 'not_found';
        })()"`);
        await sleep(8000);

        // Check success
        const finalUrl = run('agent-browser eval "location.href"');
        if (finalUrl.includes('success')) {
          console.log('  ✅ Applied successfully!');
          applied++;
          results.push({ job: job.text, status: 'success' });
        } else {
          console.log('  ❌ Apply failed (not on success page)');
          failed++;
          results.push({ job: job.text, status: 'failed' });
        }
      } else {
        console.log('  ❌ Did not reach review page');
        failed++;
        results.push({ job: job.text, status: 'failed' });
      }

    } catch (e) {
      console.log('  ❌ Error:', e.message);
      failed++;
      results.push({ job: job.text, status: 'error', error: e.message });
    }
  }

  // Summary
  console.log('\n=== SUMMARY ===');
  console.log(`Applied: ${applied}/${jobLinks.length}`);
  console.log(`Failed: ${failed}/${jobLinks.length}`);
  results.forEach(r => console.log(`  ${r.status === 'success' ? '✅' : '❌'} ${r.job} - ${r.status}`));

  // Save results
  const reportPath = `/tmp/jobstreet_apply_${Date.now()}.json`;
  fs.writeFileSync(reportPath, JSON.stringify({ search, location, results, applied, failed }, null, 2));
  console.log(`\nReport saved to: ${reportPath}`);

  // Clean up
  run('agent-browser close 2>/dev/null');
  try { execSync('pkill -f Xvfb'); } catch (e) {}
  console.log('\nDone!');
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
