# Lesson format

One lesson = one line. If you can't say it in one line, it's probably two lessons (or too vague to be useful).

## The line

```
- YYYY-MM-DD [tag][tag] <RULE in the imperative> — <why, ≤12 words>
```

- **Date** — when learned. Lets you spot stale rules and resolve conflicts (newer wins).
- **Tags** — for scoping and fast lookup. Use 1–3. Common axes:
  - tool: `[bash]` `[git]` `[edit]` `[mcp]` `[web]`
  - tech/domain: `[react]` `[python]` `[swift]` `[css]` `[sql]` `[video]` `[seo]`
  - skill: `[skill:web-craft]` `[skill:remotion-video]` (when the lesson is about using another skill)
  - phase: `[deploy]` `[test]` `[release]`
- **RULE** — imperative and concrete. "Run `X` before `Y`", "Never do Z", "Prefer A over B because…".
- **why** — the reason, short. The reason is what lets future-you apply the rule with judgment instead of
  cargo-culting it.

## Good vs weak

```
GOOD  - 2026-06-21 [bash][git] Never force-push several repos in one session — trips GitHub's anti-abuse flag.
GOOD  - 2026-06-21 [skill:desktop-panel] Keep skill `description` ≤1024 chars — the panel rejects longer ones.
GOOD  - 2026-06-21 [react][video] Animate in canvas/WebGL, not DOM — DOM can't be captured with captureStream.

WEAK  - Be more careful with git.                         (not actionable)
WEAK  - The deploy failed yesterday.                      (an event, not a rule)
WEAK  - Remember to test things.                          (too vague to change behavior)
```

A lesson is good when, read cold months later, it tells you exactly what to do differently — and why.

## Ledger file shape

```markdown
# never-again — lessons (global)

> One line per lesson. Newest at the bottom of each section. Keep it lean — see the never-again skill.

## Workflow & tools
- 2026-06-21 [bash][git] Never force-push several repos in one session — trips GitHub's anti-abuse flag.

## Language / framework gotchas
- 2026-06-21 [react][video] Animate in canvas/WebGL, not DOM — DOM can't be captured with captureStream.

## Per-skill
- 2026-06-21 [skill:desktop-panel] Keep skill `description` ≤1024 chars — the panel rejects longer ones.
```

Sections are optional but help once you have more than ~10 lessons. Group by the axis that makes recall
fastest for your work (usually tool/domain).
