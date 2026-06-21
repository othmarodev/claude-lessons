---
name: never-again
description: |
  Automatic lessons-learned memory for Claude Code — it detects your real mistakes, reworks, and corrections
  from the session transcript, turns each into one concise rule, and recalls them every session so the same
  mistake never happens twice. Zero database, zero API, zero background daemon — just markdown + hooks. Use and
  trigger this WHENEVER: there are pending candidates in the INBOX to review; the user corrects, rejects, or
  reverts your work; a command/test/build fails because of your mistake; you repeat something you already got
  wrong; you break an already-stated rule (CLAUDE.md, a memory, a prior instruction); or the user says "never do
  that again", "you keep doing X", "remember this", "don't repeat that", "log this lesson". Also recall and APPLY
  relevant lessons before risky, repeated, or previously-failed actions. Lessons live in a global + per-project
  ledger, both auto-injected each session. Project-agnostic — not tied to any one product.
---

# never-again — detect a mistake once, never repeat it

A retrospective memory with **automatic capture**. Four moves:

1. **DETECT** (automatic) — a `Stop` hook scans each finished session for rework signals (user corrections, a
   file rewritten 3+ times, a command that errored) and stages candidates in `~/.claude/never-again/INBOX.md`.
2. **CURATE** — next session, you review those candidates: keep the real, generalizable ones, discard noise.
3. **RECALL** (automatic) — a `SessionStart` hook injects the ledger(s) into context every session.
4. **APPLY** — consult the matching rule before a risky, repeated, or previously-failed action.

The detector finds the *signal*; you supply the *judgment* (phrasing + keep/discard). That split is the whole
trick: capture is automatic, but the ledger stays curated and lean instead of filling with machine noise.

## The niche (say it plainly)

Other memory tools either capture manually (you have to notice every mistake yourself) or capture
automatically but drag in a database, an API/SDK call, a vector store, or a background process. never-again is
the **lean** one: automatic transcript-grounded capture with **nothing but markdown files and two hooks**. No
network, no daemon, no lock-in — `cat ~/.claude/never-again/LESSONS.md` is the entire database.

## Reviewing the INBOX (do this when candidates are pending)

When SessionStart says there are pending candidates, or the user asks, open `~/.claude/never-again/INBOX.md`.
For each `- [ ]` candidate:

- **Is it a real, avoidable, generalizable mistake?** If it was a transient failure, the user just changing
  their mind, or a one-off that couldn't be foreseen — **discard it** (delete the line).
- If real, **phrase it as one durable rule** (see `references/lesson-format.md`) and append it to the right
  ledger: global if it's true everywhere, project-scoped if it's about this repo.
- **Dedupe**: if an existing lesson already covers it, sharpen that one instead of adding a near-duplicate.
- **Delete the candidate from the INBOX** once handled, so it doesn't resurface.

Keep a light touch — a few good rules beat many noisy ones. It is correct and expected to discard most
candidates; the detector errs toward surfacing, you err toward keeping the bar high.

## Manual capture (the detector isn't the only path)

Also capture directly — without waiting for the inbox — when you clearly just made an avoidable mistake:

- The user **corrects, rejects, or reverts** your work, or says "don't do that again".
- A **command/test/build/lint failed because of your mistake** and you had to redo it.
- You **violated a rule** that was already written down.

**Do NOT capture** transient/external failures, the user simply changing their mind, normal exploration, or
anything an existing lesson already covers. This restraint is what keeps the ledger trustworthy.

## Capture format

One line, dated, tagged, imperative, with a short *why*. Full scheme + examples: `references/lesson-format.md`.

```
- 2026-06-21 [bash][git] Never force-push several repos in one session — trips GitHub's anti-abuse flag.
- 2026-06-21 [react][video] Animate in canvas/WebGL, not DOM — captureStream can't record DOM/CSS animations.
```

## Where lessons live (two tiers, both auto-recalled)

- **Global:** `~/.claude/never-again/LESSONS.md` — rules true everywhere. Injected every session.
- **Project:** `<project>/.claude/never-again/LESSONS.md` — rules for this codebase only. Injected when you're
  in that project (the hook reads `$CLAUDE_PROJECT_DIR`). Scope ruthlessly so one repo's quirks never leak
  into another's context.

## Recall and apply

The hooks inject both ledgers for you at session start — you don't have to fetch them. Your job is the
**moment of application**: before a risky, repeated, or previously-failed action, check the matching rule and
follow it. If a lesson is now wrong or obsolete, fix or delete it — a stale rule misleads worse than none.

## Keep it lean (the part that makes it a net win)

A ledger that only grows becomes a tax on every session. The discipline — one line each, dedupe, generalize
several specifics into one rule, **graduate** rock-solid rules into `CLAUDE.md` then drop them, prune the
obsolete — lives in `references/consolidation.md`. Read it when the ledger passes a screenful. A healthy
ledger is readable in under a minute and every line would change a decision.

## Honest framing (don't oversell)

- The real, demonstrable payoff is **not repeating rework** — that saves the user's time directly. Token
  savings are a *secondary, conditional* effect: they're net-positive only when the ledger stays lean and the
  lessons actually recur, because recall does cost some tokens every session. Lead with "stops repeated
  mistakes," not "saves tokens."
- Detection is heuristic, not perfect — it surfaces candidates; your curation makes them trustworthy.
- The detector needs `python3` (standard on macOS/Linux). Without it, auto-capture is skipped and manual
  capture + recall still work. Recall itself is pure bash and always works.

## Project-agnostic

Applies to **any** project, current or future. Tag and scope per project; never assume one specific product.
