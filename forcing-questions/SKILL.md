---
name: forcing-questions
description: Use before answering questions, decomposing tasks, or proposing solutions where the framing itself might be wrong. Pushes back on hidden assumptions, scope creep, and overengineering at the conversation level. Not for greenfield design specs (use brainstorming), not for implementation plans (use writing-plans).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, pushback, framing, scope, design, workflow]
    related_skills: [brainstorming, writing-plans, plan, debug]
---

# Forcing Questions

## Overview

A lightweight pushback layer for ambiguous or high-stakes requests. Before answering, decomposing, or proposing, run the 4 questions internally and surface the answers that actually matter for the user's decision.

This is **not** a spec-driven design framework (use `brainstorming` for that) and **not** an implementation planner (use `writing-plans`). It runs **before both** — at the point where the user is still framing the problem. The goal is to surface bad framing, overengineering, and unexamined assumptions early, when they're cheap to fix.

Built from synthesis of three sources:

- **obra/superpowers** `brainstorming` — scope check, one-question-at-a-time, propose 2-3 approaches
- **gsd-build/get-shit-done** discuss phase — purpose / current state / constraints / success criteria
- **garrytan/gstack** `/office-hours` — adversarial challenge to the user's premise

Adapted for **conversational multi-profile dispatch** (Hermes kanban, Telegram-chat-driven) — not greenfield project design.

## When to Use

**Use when:**

- User asks a question whose answer depends on hidden assumptions
- User proposes a solution that smells overengineered or has unclear scope
- User says "build X" where X is actually multiple independent subsystems
- Task has high cost-of-failure (production change, money, irreversible action)
- User explicitly invokes `/force` or asks you to challenge their framing
- You're about to decompose work into profiles / subagents and want to validate the decomposition

**Don't use for:**

- Greenfield design specs → use `brainstorming` (full spec doc, 2-3 approaches, design sections)
- Implementation plans → use `writing-plans` (bite-sized tasks, exact code)
- Quick factual answers — running the 4 questions is overhead
- Trivial actions the user has clearly already thought through
- When user is mid-execution and asking for the next concrete step (gates kill momentum)

## The 4 Forcing Questions

Run all 4 in order. Surface 1-3 to the user — the ones that change the decision. Skip the rest.

### 1. Scope Check

> Is this ONE task, or multiple independent subsystems disguised as one?

The most common failure mode. User says "build me a kanban with chat, file uploads, and notifications" — that's 3-4 projects, not 1. Decomposing early saves hours of work that gets thrown away.

**Surface to user when:** request contains >1 noun-phrase capability, "and", "with", or vague "platform" framing.

**How to surface:**

```
Scope check: ini 1 task atau beberapa? gue baca sebagai:
- [task A] — [one line]
- [task B] — [one line]
- [task C] — [one line]

Kalau bener, mana yang mau di-handle duluan? Atau lo emang mau 1 project yang nge-cover semua?
```

**Skip when:** request is clearly single-purpose ("fix this bug", "add this field").

### 2. Framing Check

> What is the user actually trying to accomplish, separate from the solution they proposed?

Users often conflate problem and solution. "Build a forcing-questions skill" might actually be "I keep getting bad answers from agents" — the skill is a proposed solution, not the problem.

**Surface to user when:** request includes a specific solution/implementation AND the problem isn't explicit.

**How to surface:**

```
Framing check: gue baca request lo sebagai [problem Y], dengan proposed solution [X]. Bener, atau:
- Problem-nya beda?
- Ada constraints yang gue miss?
- "Success" buat lo itu apa konkretnya (gak abstract)?
```

**Skip when:** user stated the problem clearly before proposing a solution ("I keep hitting X, so let's try Y").

### 3. Constraint / One-Thing Check

> If you could only ship ONE thing, what would it be?

Kills overengineering at the gate. Real fix for "user rejected 4-system proposal as overengineered" pattern. Most overbuilt solutions are 3-4 features where 1 would have taught the user what they actually needed.

**Surface to user when:** proposed solution has >1 component, or you're about to suggest a multi-piece plan.

**How to surface:**

```
Kalau lo cuma boleh ship SATU, mana yang paling impactful? Sisanya bisa loop-in nanti kalau yang pertama jalan.

[y] vs [z] trade-off: [brief].
```

**Skip when:** scope is already minimal.

### 4. Reversibility Check

> If this is wrong, how expensive is rollback?

Drives the depth-of-discussion decision. Cheap-to-reverse = execute first, learn from result. Expensive-to-reverse = design before building.

**Surface to user when:** you're about to spend significant time on something where the cost of being wrong is high.

**Internal heuristic** (don't always surface to user, use to decide your own depth):

| Reversibility | Action |
|---|---|
| Trivial (config, draft, scratch file) | Execute, iterate from result |
| Cheap (branch, can revert) | Brief framing check, then execute |
| Medium (deployed, visible to others) | Full 4 questions, propose 2-3 approaches |
| Expensive (production data, money, irreversible) | Full 4 questions + design doc + explicit approval gate |

## Output Format

When you surface forcing questions to the user, structure your response:

```markdown
[Bukan eksekusi dulu — beberapa forcing question]

1. **Scope:** [question or statement]
2. **Framing:** [question or statement]
3. **Constraint:** [question or statement]
4. **Reversibility:** [cheap / medium / expensive — brief note]

[Lanjutkan dengan minimum context, atau stop dan tunggu jawaban]
```

**Rules:**

- One question at a time if you MUST ask, not all 4 in a wall (use `brainstorming` if user wants that flow)
- Multiple-choice preferred for the question you're actually asking
- If only 1-2 questions matter, drop the rest — don't pad
- Stop and wait for response. Do NOT proceed to decomposition before the gating question is resolved.

## Anti-Patterns

**Don't:**

- Run forcing questions on every trivial message — overhead kills trust
- Ask all 4 when only 1 is the real blocker
- Treat forcing questions as a workaround for "I don't know" — they sharpen, they don't replace thinking
- Couple with brainstorming flow (overkill) — pick ONE layer
- Use as stalling tactic when user is ready to execute

**Do:**

- Pick the highest-leverage question and lead with it
- Mark when you're invoking this skill ("running forcing-questions first...")
- Skip silently when the request is clear and bounded

## Integration With Other Skills

```
User request
    ↓
forcing-questions          ← YOU ARE HERE (chat-level framing)
    ↓
brainstorming              ← greenfield design (spec doc, 2-3 approaches)
    ↓
writing-plans              ← implementation plan (bite-sized tasks)
    ↓
subagent-driven-development ← execution
    ↓
requesting-code-review     ← verification
```

**Use forcing-questions when:** the user is still framing the conversation, dispatching work, or making a decision.

**Use brainstorming when:** user has a concrete project and you need to produce a design spec.

**Use writing-plans when:** you have a design and need to plan implementation.

**Use subagent-driven-development when:** you have a plan and need to execute.

Don't combine forcing-questions with brainstorming in the same turn — pick the layer that matches where the user actually is.

## Quick Reference

| Signal in user request | Run forcing-questions? | Surface which? |
|---|---|---|
| "Build X with Y and Z" | Yes | Q1 (Scope) |
| "I think we should use <tech>" | Yes | Q2 (Framing) |
| "Add <feature>" (multi-component) | Yes | Q3 (Constraint) |
| "Ship this to production" | Yes | Q4 (Reversibility) — full check |
| "Fix this bug" | No | — |
| "What is X?" (factual) | No | — |
| "Continue with the next step" | No | — |
| "Why did you do X?" (debugging) | No (use `debug`) | — |

## Example

**User:** "Gue kepikiran bikin forcing-questions skill buat ngurangin overengineering."

**Without forcing-questions skill (default behavior):**

> Sip, gue bikin. Bentar ya...
> [proceeds to build full framework, 23 skills, 9452 tests, 60+ files]

**With forcing-questions skill (correct behavior):**

```
[Bukan eksekusi dulu — 2 forcing question yang matter]

1. **Scope:** "forcing-questions" ini 1 skill atau bakal jadi sistem? Kalau sistem, decompose dulu — kita diskusikan 1 skill dulu, framework-nya belakangan.

2. **Framing:** gue baca sebagai: lo sering dapet jawaban overengineered/over-scope dari gue. Bener? Atau ada masalah lain di belakang request ini?

Constraint: kalau cuma boleh 1 skill, ini dia — atau ada skill lain yang lebih impactful duluan?

[gak lanjut sampe 2 pertanyaan di atas kejawab]
```

User clarifies → proceed to brainstorming or writing-plans. Skip the 4-question ritual on the *next* exchange if context is now clear.

## Notes

This skill deliberately does NOT include:

- A spec template — use `brainstorming` for that
- A plan format — use `writing-plans` for that
- A question database / library — keeps the skill small, surfaces force at the right level
- A scoring rubric — forcing questions are heuristic, not algorithmic

If a forcing question is being repeated across sessions, that's signal to either (a) promote it to a JARVIS persona rule, or (b) investigate why the upstream framing keeps producing it.
