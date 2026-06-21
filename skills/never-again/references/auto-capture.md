# Automatic capture — how detection works

The `Stop` hook (`hooks/stop` → `hooks/detect-rework.py`) runs after each session ends. It reads the session
transcript, scans the recent messages for **rework signals**, and stages candidates into
`~/.claude/never-again/INBOX.md`. It never writes lessons directly — only signals for you to curate. It fails
open (silent) so it can never block a stop, and skips itself entirely if `python3` is absent.

## What it detects (conservative — precision over recall)

1. **User corrections** — a genuine human turn matching rework phrasing (EN + ES): "no,", "that's wrong",
   "revert", "you keep…", "don't do that", "that broke…", "otra vez", "está mal", "te equivocaste", etc.
   This is the strongest signal that you got something wrong.
2. **File churn** — the same file edited 3+ times in one session, which usually means a wrong first approach.
3. **Errored commands** — a tool result flagged `is_error`, i.e. something failed.

It stages at most **3 candidates per session**, and deduplicates against both the existing ledger and the
inbox (by a normalized key of the first ~40 characters) so the same signal never piles up.

## The inbox lifecycle

```
session ends ──► Stop hook detects signals ──► appends "- [ ] (kind) snippet" to INBOX.md
                                                          │
next session starts ──► SessionStart hook says "N pending candidates"
                                                          │
you review (never-again skill) ──► keep real ones as one-line lessons ──► delete handled candidates
```

## Curating well

The detector is deliberately noisy at the edges — that's fine, because curation is cheap and keeps the ledger
trustworthy. When reviewing:

- **Discard generously.** Transient errors, the user changing their mind, exploration, and one-offs are not
  lessons. Most candidates should be deleted. That is the system working, not failing.
- **Generalize.** Turn "that specific command failed" into the underlying rule ("run X before Y because…").
- **Scope.** A repo-specific quirk goes in that project's ledger, not global.
- **Dedupe.** Strengthen an existing lesson rather than adding a near-twin.
- **Clear the inbox.** Delete each candidate after handling so it doesn't resurface next session.

## Tuning

To change sensitivity, edit `hooks/detect-rework.py`:
- `CORRECTION_RE` — the phrase patterns (add your own language/idioms).
- `MAX_CANDIDATES` — cap per session (default 3).
- `TAIL_MESSAGES` — how far back to scan (default 60).

Keep it conservative. A detector that surfaces 1 real lesson and 1 false positive is healthy; one that floods
the inbox trains you to ignore it.
