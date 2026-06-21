# never-again — lessons (example, populated)

> A realistic ledger after a few weeks of use. Yours grows from your own mistakes — this just shows the shape.
> Format: `- YYYY-MM-DD [tag][tag] <imperative rule> — <why, ≤12 words>`

## Workflow & tools
- 2026-06-02 [git] Never force-push several repos in one session — trips GitHub's anti-abuse flag.
- 2026-06-05 [git] Don't rebase a branch others have pulled — it rewrites shared history and breaks their clones.
- 2026-06-09 [bash] Quote variables in `rm`/`mv` paths (`rm "$x"`) — an unset/glob var can wipe the wrong files.
- 2026-06-11 [bash][ci] Check the runner's tool versions before `npm ci` — a Node mismatch fails the whole job.
- 2026-06-14 [github] Create at most a couple of repos per day on a young account — bursts look like bot spam.

## Language / framework gotchas
- 2026-06-03 [react][video] Animate in canvas/WebGL, not DOM — captureStream can't record DOM/CSS animations.
- 2026-06-06 [react] Don't put `Math.random()`/`Date.now()` in render — breaks deterministic output and tests.
- 2026-06-08 [python] Activate the venv before `pip install` — installing into system Python pollutes the host.
- 2026-06-10 [sql] Never run UPDATE/DELETE without a WHERE in prod — one missing clause rewrites every row.
- 2026-06-12 [ts] Validate external input with a schema at the boundary — trusting shape causes runtime crashes.

## Build / deploy
- 2026-06-07 [ffmpeg] Add `-pix_fmt yuv420p` to H.264 MP4 — without it some players show a black video.
- 2026-06-13 [env] Keep secrets server-side only; expose only `PUBLIC_*` vars — anything else leaks to the client.
- 2026-06-15 [deploy] Confirm the billing/quota is active before a paid API call — free tiers can be quota 0.

## Per-skill / integrations
- 2026-06-04 [skill][panel] Keep a skill `description` ≤1024 chars — the desktop panel rejects longer ones.
- 2026-06-16 [gemini][billing] Gemini image models have free-tier quota 0 — needs a prepaid/billed project.
