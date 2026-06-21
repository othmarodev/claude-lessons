# Consolidation — keeping the ledger lean

This is the mechanism that makes never-again *save* tokens instead of spending them. A ledger that only grows
becomes a tax on every session. Run this pass whenever the ledger passes ~40 lines / a screenful, or feels
repetitive.

## Budget

- **One line per lesson.** No multi-line entries. If it needs more, it's two lessons or it belongs in a doc.
- **Soft cap the global ledger** at ~30–50 lessons / ~3 KB. Project ledgers can be a bit larger but still tight.
- If you're over budget, you must consolidate before adding more — the cap forces quality over accumulation.

## The five moves

1. **Dedupe** — merge near-duplicates into one sharper rule. Two lessons about the same root cause = one lesson.
2. **Generalize** — if several specific lessons share a cause, replace them with one general rule.
   *e.g.* three "escape quotes in X / Y / Z" lessons → "Always escape user strings before embedding in JSON."
3. **Graduate** — a rule that is now rock-solid and always-applies should be **promoted into `CLAUDE.md`**
   (project) or the user's global rules, then **removed from the ledger**. Graduated rules are "baked in" and
   no longer need to ride in the ledger. This is the main pressure-release valve.
4. **Prune** — delete obsolete lessons: the tool changed, the file was deleted, the rule no longer applies.
   A stale rule is worse than no rule because it misleads.
5. **Scope down** — a lesson that's really project-specific but landed in global → move it to the project ledger.

## When two lessons conflict

Newer date wins, but investigate why they conflict — usually the older one needs pruning or the newer one
needs a narrower scope (a tag/condition) so both can coexist truthfully.

## The test for a healthy ledger

You can read the whole thing in under a minute, every line would change a decision, and nothing in it is
already enforced elsewhere (CLAUDE.md, a linter, a test). If a lesson is enforced by tooling now, prune it —
the tooling is the better memory.
