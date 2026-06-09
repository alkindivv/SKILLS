---
name: debug
description: "Use when debugging, troubleshooting, investigating errors, fixing bugs, or diagnosing issues. Trigger on: 'debug', 'fix bug', 'error', 'broken', 'not working', 'crash', 'fail', 'issue', 'problem', 'troubleshoot', 'diagnose', 'investigate'. Produces definitive root cause analysis with exact line tracing and failure chain reconstruction."
---

# Debug Skill

When debugging, the standard isn't "I found something" — it's "holy shit, that's exactly why it broke."

## Core Philosophy

The marginal cost of completeness is near zero. Go all the way. Cover the whole failure surface.

- Cover it with primary sources — actual stack traces, actual log lines, actual code paths, not paraphrases
- Cover it with contradicting hypotheses
- Cover it so thoroughly that the root cause is definitively isolated, not merely plausible
- Never offer to table a line of investigation when the answer is within reach
- Never leave a hypothesis untested when disconfirming it takes five more minutes
- Never surface a surface-level "could be X" when the actual execution path exists in the code

Trace before concluding. Reproduce before asserting. Triangulate across call stack, state, and environment before committing to a root cause claim.

## What "Complete" Means

- Root cause is traced to the **exact line**, not the approximate module
- The failure chain is reconstructed end-to-end: trigger → propagation → symptom
- Contradicting hypotheses are surfaced and falsified, not buried
- Environment assumptions (runtime, deps, config, state) are made explicit
- Quantitative claims (latency, memory, error rate) carry their measurement context
- If the bug space feels too large, decompose it and finish every sub-hypothesis in this turn

## Output Structure

Every debug output MUST include:

### 1. Root Cause
The exact broken invariant. Not "it might be X" — the definitive "this is why it broke" with the exact line reference.

### 2. Failure Chain
End-to-end reconstruction:
```
Trigger → [step 1] → [step 2] → ... → Symptom
```
Each step must reference specific code, state, or conditions.

### 3. Steel-man Alternative
The strongest alternative root cause, and **why it's ruled out** with evidence.

### 4. Peta Ketidakpastian
- **Dikonfirmasi**: Fakta yang sudah diverifikasi dengan bukti langsung
- **Disimpulkan**: Kesimpulan dari bukti, tapi belum langsung dikonfirmasi
- **Tidak Diketahui**: Hal yang butuh investigasi lebih lanjut

### 5. "Jadi Apa?" (So What)
- The exact fix (code change, config change, etc.)
- The regression test that would catch this
- Systemic change (if any) to prevent recurrence

## Debug Workflow

1. **Reproduce** — Can you make it happen reliably? What are the exact steps?
2. **Isolate** — Narrow down the failure surface. Binary search the code.
3. **Trace** — Follow the execution path. Read the actual code, not your assumptions about it.
4. **Hypothesize** — Generate multiple hypotheses. Don't anchor on the first one.
5. **Falsify** — Try to disprove each hypothesis. The one that survives is your root cause.
6. **Verify** — Confirm the root cause explains ALL observed symptoms, not just some.
7. **Fix** — Implement the minimal fix. Write a regression test.
8. **Prevent** — Is there a systemic issue? Add guardrails if needed.

## Investigation Techniques

### Binary Search
Comment out or disable half the code. Does the bug persist? Narrow down iteratively.

### Print/Log Debugging
Add strategic logging at decision points. Don't guess what the code does — observe it.

### State Inspection
What's the actual value of variables at the failure point? Don't assume — check.

### Stack Trace Analysis
Read from the bottom up. The first frame is usually the symptom, not the cause.

### Differential Debugging
What changed? Git diff, recent deploys, config changes. Bugs don't appear from nothing.

## Anti-Patterns

- "Ini mungkin karena..." — Punya bukti? Tunjukkan. Tidak punya? Akui.
- "Coba restart" — Itu workaround, bukan fix. Kenapa restart diperlukan?
- "Kode ini seharusnya bekerja" — Tapi tidak bekerja. Mengapa?
- "Sudah saya coba dan berhasil" — Di environment yang sama? Dengan data yang sama?
- "Ini bug di library" — Buktikan. Baca source code librarynya.

## Quality Checklist

Sebelum menyelesaikan debug, pastikan:

- [ ] Root cause di-trace ke baris kode spesifik
- [ ] Failure chain lengkap dari trigger ke symptom
- [ ] Hipotesis alternatif sudah difalsifikasi dengan bukti
- [ ] Environment assumptions dinyatakan eksplisit
- [ ] Ada regression test yang akan menangkap bug ini jika muncul lagi
- [ ] Ada rekomendasi pencegahan jika ini masalah sistemik
