---
name: implementing
description: "Use when implementing features, fixing bugs, writing code, or making changes to codebase. Trigger on: 'implement', 'add feature', 'fix', 'change', 'update', 'refactor', 'write code', 'build', 'create', 'make'. Enforces KISS, YAGNI, TDD principles. ALWAYS use this skill when working on code — even simple changes benefit from this discipline."
---

# Implementation Skill

When implementing code, the standard isn't "good enough" — it's "holy shit, that's done."

## Core Philosophy

The marginal cost of completeness is near zero with AI. Do the whole thing. Do it right. Do it with tests. Do it with documentation. Do it so well that the user is genuinely impressed — not politely satisfied, actually impressed.

- Never offer to "table this for later" when the permanent solve is within reach
- Never leave a dangling thread when tying it off takes five more minutes
- Never present a workaround when the real fix exists
- If it works in 1 line, don't make it 10 lines
- Search before building. Test before shipping. Ship the complete thing

Time is not an excuse. Fatigue is not an excuse.

## KISS — Keep It Simple, Stupid

- One function = one job. Describe it in one sentence or split it.
- Max 25 lines per function. If longer, extract helper.
- No clever one-liners. Readability beats compactness.
- Boring code is good code. If a junior dev can't read it in 10 seconds, rewrite it.

## YAGNI — You Aren't Gonna Need It

- Do NOT build features not in the current task
- Do NOT create abstractions for "future use cases"
- Do NOT add config options nobody asked for
- Do NOT refactor code that works unless the task requires it
- If only one place uses it, it stays inline. No shared utils.

## TDD — Test-Driven Development (ALWAYS)

Follow RED → GREEN → REFACTOR. No exceptions. No shortcuts.

1. **RED**: Write the failing test FIRST. Show the failure.
2. **GREEN**: Write MINIMUM code to pass. Nothing more.
3. **REFACTOR**: Only after green. Confirm green again.

Rules:
- Every commit includes tests. No test = no commit.
- Test BEHAVIOR (input → output), not implementation (internal calls).
- If you can't write a test, you don't understand the requirement yet.

## Workflow

1. **Understand** — Read existing code, search for patterns, understand the architecture
2. **Plan** — Identify the minimal change needed. Don't over-engineer.
3. **Test First** — Write the failing test that defines the expected behavior
4. **Implement** — Write the minimum code to pass the test
5. **Refactor** — Clean up only after tests pass. Keep it simple.
6. **Verify** — Run all tests, not just yours. Check for regressions.
7. **Ship** — Commit with clear message. Done means done.

## Anti-Patterns to Avoid

- "Let me add this utility function in case we need it later" → YAGNI
- "I'll just skip the test for this one" → TDD violation
- "This is a small change, no need to test" → All changes get tests
- "Let me refactor this unrelated code while I'm here" → Scope creep
- "I'll come back to fix this later" → Fix it now or don't touch it
