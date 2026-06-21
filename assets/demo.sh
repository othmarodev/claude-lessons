#!/usr/bin/env bash
# Scripted terminal demo of never-again preventing a repeated mistake.
# Used by assets/demo.tape (vhs) to render assets/demo.gif. Pure echo + sleep — no real commands.
set -u
V='\033[38;5;141m'; G='\033[38;5;114m'; B='\033[38;5;75m'; A='\033[38;5;179m'; D='\033[38;5;245m'; W='\033[38;5;252m'; N='\033[0m'
p(){ printf "$1\n"; sleep "${2:-0.7}"; }

p "${D}── session 1 ──────────────────────────────────────────────${N}" 0.8
p "${B}you ▸${N} ${W}no — don't force-push all my repos, you flagged my GitHub${N}" 1.4
p "${V}      ✎ never-again captured a lesson${N}" 0.9
p "${D}      LESSONS.md ${G}+ [git] Never force-push several repos in one session${N}" 1.6
p ""
p "${D}── session 2  ·  a week later ─────────────────────────────${N}" 0.8
p "${V}⟳ SessionStart${N} ${D}· never-again loaded 12 lessons${N}" 1.3
p "${B}you ▸${N} ${W}push the fixes to all five repos${N}" 1.4
p "${A}claude ▸${N} ${W}⏸ a saved lesson says never force-push multiple repos at once.${N}" 1.0
p "${W}          pushing them one at a time instead.${N}" 1.6
p ""
p "${G}✓ the mistake did not happen again.${N}" 1.0
p "${D}  no database · no API · no daemon — just markdown + two hooks${N}" 2.0
